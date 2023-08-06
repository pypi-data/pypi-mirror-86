import os

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import File
from django.db import models
from django.db.models import CASCADE
from django.db.models.deletion import SET_NULL
from django.db.models.fields.files import ImageFieldFile, FieldFile
from django.utils.functional import cached_property
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel, ActivatorModel

from orionframework.authored.models import AuthoredModel
from orionframework.indexable.models import IndexedModel
from orionframework.taggable.models import TaggableModel
from orionframework.utils.files import get_random_name
from orionframework.utils.reflection import get_class

ON_DELETE = getattr(settings, 'ORION_MEDIA_ON_DELETE', CASCADE)
MEDIA_CATEGORY_CHOICES = getattr(settings, "ORION_MEDIA_CATEGORY_CHOICES", None)
MEDIA_PATH = getattr(settings, "ORION_MEDIA_PATH", "uploads/documents")
MEDIA_PATH_RESOLVER_CLASS = get_class(getattr(settings, "ORION_MEDIA_PATH_RESOLVER",
                                              "orionframework.media.path_resolvers.MediaPathResolver"))
MEDIA_PATH_RESOLVER = MEDIA_PATH_RESOLVER_CLASS(path=MEDIA_PATH)

DOCUMENT_MODEL_NAME = getattr(settings, "ORION_MEDIA_DOCUMENT_MODEL_NAME", "media.Document")
IMAGE_MODEL_NAME = getattr(settings, "ORION_MEDIA_DOCUMENT_MODEL_NAME", "media.Image")


class Media(IndexedModel,
            TitleDescriptionModel,
            ActivatorModel,
            TimeStampedModel,
            AuthoredModel,
            TaggableModel):
    """
    Abstract class common to both document or image models.
    
    @since: 05/10/2016 19:50:00
    
    @author: orionframework
    """

    class Meta:
        abstract = True

    filename = models.CharField(max_length=200, null=True, blank=True)
    """
    The original file name if needed to be used for anything
    """

    filesize = models.IntegerField(null=True, blank=True)
    """
    The number of bytes for the original file (size).
    """

    parent_id = models.CharField(db_index=True, max_length=200, null=True, blank=True)
    """
    The parent model's identifier.
    """

    parent = GenericForeignKey('parent_type', 'parent_id')
    """
    The actual parent object storing this document.
    """

    category = models.IntegerField(db_index=True, null=True, blank=True, choices=MEDIA_CATEGORY_CHOICES)
    """
    The category used to group the image in the target model.
    """

    origin_url = models.URLField(null=True, blank=True, max_length=1000)
    """
    The URL from where this image was originally imported.
    """

    origin_id = models.CharField(null=True, blank=True, max_length=255, db_index=True)
    """
    An extra bit of information about the origin of this image.
    """

    def __init__(self, *args, **kwargs):

        super(Media, self).__init__(*args, **kwargs)

        if self.pk:
            self.old_file = self.file
        else:
            self.old_file = None

    def __str__(self):
        return self.title

    # @property
    # def parent(self):
    #    return self.parent_type.get_object_for_this_type(id=self.parent_id)

    @property
    def url(self):

        return self.file.url

    @property
    def urls(self):

        return {
            "original": self.file.url
        }

    @property
    def extension(self):

        name, extension = os.path.splitext(self.filename)

        return extension[1:].lower()

    @cached_property
    def storage(self):
        return self._meta.get_field('file').storage

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.file != self.old_file and self.file and (update_fields is None or "file" in update_fields):

            self.filename = self.get_file().name
            self.filesize = self.get_file().size

            if self.old_file:
                # delete existing file so we can override it
                self.delete_file(self.old_file)

                #
                self.file.name = self.old_file.name

            self.file.name = get_random_name(self.filename)

        return super(Media, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                       update_fields=update_fields)

    def get_file(self):

        if isinstance(self.file, FieldFile):
            return self.file.file

        return self.file

    def copy(self, **kwargs):

        new_file = File(self.file.storage.open(self.file.name))

        copy = super(Media, self).copy(file=new_file, old_file=None, **kwargs)

        return copy

    def resolve_path(self, filename, resolver):
        """
        Method called finally resolve the location where this file should be stored.
        At first, the path is resolved by the framework over the orion's MEDIA_PATH_RESOLVER settings
        but ultimately models have the ability to override this if necessary.

        For more info, see orion.media.path_resolvers

        @return the resolved filepath for the given filename under this model. If nothing is returned
        then the logic is delegated up to the configured settings instead.
        """
        return None


class AbstractDocument(Media):
    """
    Model used to map an image uploaded/attached to another model in the system.
    
    @since: 06/17/2016 20:30:00
    
    @author: orionframework
    """

    parent_type = models.ForeignKey(ContentType, on_delete=ON_DELETE, null=True, blank=True, related_name="documents")
    """
    The type bound to this document
    """

    file = models.FileField('The document itself', upload_to=MEDIA_PATH_RESOLVER, max_length=500)
    """
    The image itself
    """

    preview = models.OneToOneField(IMAGE_MODEL_NAME, on_delete=SET_NULL, null=True, blank=True,
                                   related_name="preview_source")
    """
    If preview tools are installed, this stores the reference of the image used to preview the document's content. 
    """

    class Meta:
        abstract = True

    @property
    def type(self):
        return "document"

    def to_json(self, thumbnail_name=None):

        return {
            "id": self.id,
            "title": self.title,
            "url": self.file.url
        }

    def delete_file(self, _file):

        if isinstance(_file, FieldFile):

            self.storage.delete(_file.name)

        elif isinstance(_file, str):

            self.storage.delete(_file)


class AbstractImage(Media):
    """
    Model used to map an image uploaded/attached to another model in the system.
    
    @since: 06/17/2014 20:30:00
    
    @author: orionframework
    """

    parent_type = models.ForeignKey(ContentType, on_delete=ON_DELETE, null=True, blank=True, related_name="images")
    """
    The type bound to this image
    """

    file = models.ImageField('The image itself', upload_to=MEDIA_PATH_RESOLVER, width_field="width",
                             height_field="height", max_length=500)
    """
    The image itself
    """

    thumbnails_filesize = models.IntegerField(null=True, blank=True)
    """
    The number of bytes for all the generated thumbnails.
    """

    width = models.FloatField(null=True, blank=True)
    """
    The width (in pixels) for the image
    """

    height = models.FloatField(null=True, blank=True)
    """
    The height (in pixels) for the image
    """

    class Meta:
        abstract = True

    @property
    def type(self):
        return "image"

    def to_json(self, thumbnail_name=None):

        if thumbnail_name:

            from easy_thumbnails.templatetags import thumbnail

            url = thumbnail.thumbnail_url(self.file, thumbnail_name)

        else:
            url = self.file.url

        return {
            "id": self.id,
            "title": self.title,
            "url": url
        }

    @property
    def urls(self):

        urls = {
            "original": self.file.url
        }

        from easy_thumbnails.templatetags import thumbnail
        aliases = getattr(settings, "THUMBNAIL_ALIASES", {})

        for value in aliases.values():

            for name in value.keys():
                url = thumbnail.thumbnail_url(self.file, name)

                urls[name] = url

        return urls

    def delete_file(self, _file):

        self.thumbnails_filesize = None

        if isinstance(_file, ImageFieldFile) and _file.name:

            self.storage.delete(_file.name)

        elif isinstance(_file, str):

            self.storage.delete(_file)

        try:
            from easy_thumbnails.files import get_thumbnailer

            thumbnailer = get_thumbnailer(_file)
            thumbnailer.delete_thumbnails()

        except ImportError:
            pass

    def copy(self, **kwargs):

        copy = super(AbstractImage, self).copy(**kwargs)

        aliases = getattr(settings, "THUMBNAIL_ALIASES", {})

        for value in aliases.values():

            for name in value.keys():
                copy.to_json(name)

        return copy

    def resolve_path(self, filename, resolver):

        if hasattr(self, "preview_source") and self.preview_source:
            return resolver(self.preview_source, "preview/" + filename, allow_override=False)

        return super(AbstractImage, self).resolve_path(filename, resolver)
