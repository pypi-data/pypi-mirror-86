import os
import uuid
from pathlib import Path
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.urls import reverse
from django.core.files.base import ContentFile
from taggit.managers import TaggableManager
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill

from .specs import version_specs
from .appconfig import (
    MB_STORAGE,
    MB_THUMBNAIL_FORMAT,
    MB_VERSIONS_ROOT,
)

import logging
logger = logging.getLogger(__name__)

PERMISSION_LEVELS = (
    ('e', 'Edit'),
    ('v', 'View'),
)


def image_upload_path(instance, filename):
    """file will be uploaded to MEDIA_ROOT/user_<id>/<filename>"""
    return f"user_{instance.owner.id}/images/{filename}"


def image_thumbnail_path(instance, filename):
    """file will be uploaded to MEDIA_ROOT/user_<id>/<filename>"""
    return f"user_{instance.owner.id}/thumbnails/{filename}"


def file_upload_path(instance, filename):
    """file will be uploaded to MEDIA_ROOT/user_<id>/<filename>"""
    return f"user_{instance.owner.id}/files/{filename}"


def delete_version_image(instance):
    if(not instance.versions):
        return
    for version in instance.versions:
        full_path = f"{MB_VERSIONS_ROOT}/{instance.versions[version]}"
        try:
            os.remove(full_path, exist_ok=True)
        except Exception as error:
            logger.critical(error)
    instance.versions = None


class Thumbnail(ImageSpec):
    processors = [ResizeToFill(200, 200)]
    format = MB_THUMBNAIL_FORMAT
    options = {'quality': 90}


class Node(models.Model):
    """All other models common data of this model"""
    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(_("name"), max_length=500)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Owner"), related_name="nodes",
        on_delete=models.CASCADE
    )
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("shared_with"), related_name="shared_nodes",
        through="rest_mediabrowser.NodePermission"
    )

    def __str__(self):
        return self.name


class Collection(Node):
    """collection will act like a folder"""
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Media(Node):
    """Common data for all type of media"""
    parent = models.ForeignKey(
        "rest_mediabrowser.Collection",
        verbose_name=_("collection"), related_name="files",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = TaggableManager(blank=True)
    published = models.BooleanField(_("Status"), default=False)
    published_path = models.CharField(
        _("Published Path"), max_length=500, blank=True)
    extension = models.CharField(_("Extension"), max_length=50, blank=True)

    def __str__(self):
        return f"{self.name}"

    @cached_property
    def media_data(self):
        if hasattr(self, "mediaimage"):
            return self.mediaimage
        elif hasattr(self, "mediafile"):
            return self.mediafile
        return None

    @cached_property
    def media_type(self):
        if hasattr(self, "mediaimage"):
            return "mediaimage"
        elif hasattr(self, "mediafile"):
            return "mediafile"
        return None

    @cached_property
    def get_media_url(self):
        if hasattr(self, "mediaimage"):
            return self.mediaimage.get_image_url()
        elif hasattr(self, "mediafile"):
            return self.mediafile.get_file_url()
        return None


class MediaImage(Media):
    alt_text = models.CharField(
        _("alternative text"), max_length=100, blank=True)
    height = models.IntegerField(_("height"), blank=True, null=True)
    width = models.IntegerField(_("width"), blank=True, null=True)
    image = models.ImageField(
        _("image"), upload_to=image_upload_path,
        height_field='height', width_field='width',
        max_length=500, storage=MB_STORAGE
    )
    thumbnail = models.ImageField(
        _("Thumbnail"), upload_to=image_thumbnail_path,
        max_length=500, storage=MB_STORAGE,
        null=True, blank=True
    )
    versions = models.JSONField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(MediaImage, self).__init__(*args, **kwargs)
        self.prev_image_name = self.image.name if self.image else ''
        self.prev_published = self.published

    def save(self, *args, **kwargs):
        if self.image:
            if not self.id or self.image.name != self.prev_image_name:
                delete_version_image(self)
                self.generate_thumbnail(save=False)
                self.extension = self.image.name.split('.')[-1]
            if self.prev_published and not self.published:
                delete_version_image(self)
            if not self.name:
                self.name = self.image.name
        super(MediaImage, self).save(*args, **kwargs)

    def generate_thumbnail(self, save=True):
        image_generator = Thumbnail(source=self.image)
        result = image_generator.generate()
        thumb_file = ContentFile(result.getvalue())
        self.thumbnail.save(
            f'thumbnail.{MB_THUMBNAIL_FORMAT.lower()}', thumb_file, False)
        if save:
            self.save()

    def get_version(self, version_spec="original"):
        if self.published:
            if version_spec == "original":
                return self.published_path
            else:
                # Check version existance
                SpecClass = version_specs.get(version_spec, None)
                if SpecClass is None:
                    raise Exception(
                        f"No such version \"{version_spec}\" specified in \"MEDIA_BROWSER_VERSIONS\"")
                # return path if version exist
                if self.versions and self.versions.get(version_spec):
                    return self.versions[version_spec]
                else:
                    # assign format
                    if SpecClass.format is None:
                        SpecClass.format = self.extension
                    # Assign path
                    relative_path = self.image.url.split("/")
                    file_name = f"{relative_path[-1].split('.')[0]}.{SpecClass.format}"
                    relative_path[-1] = f"versions/{version_spec}-{file_name}"
                    relative_path = "/".join(relative_path[1:])
                    full_path = f"{MB_VERSIONS_ROOT}/{relative_path}"
                    # Create dir if needed
                    full_path_obj = Path(full_path)
                    os.makedirs(full_path_obj.parent, exist_ok=True)
                    # Start conversion
                    image_generator = SpecClass(source=self.image)
                    result = image_generator.generate()
                    with open(full_path, 'wb') as ofile:
                        ofile.write(result.read())
                    # update version data
                    if(not self.versions):
                        self.versions = {}
                    self.versions[version_spec] = relative_path
                    self.save()
                    return relative_path
        else:
            raise Exception("This asset is not published")

    @property
    def ext(self):
        return self.extension if self.extension else \
            self.image.name.split('.')[-1]

    def get_image_url(self):
        return reverse("mb-image", kwargs={"slug": self.slug, "ext": self.ext})

    def get_thumbnail_url(self):
        return reverse("mb-thumbnail", kwargs={
            "slug": self.slug,
            'ext': MB_THUMBNAIL_FORMAT.lower()
        })

    def __str__(self):
        return f'{self.name}'


@receiver(pre_delete, sender=MediaImage)
def deleted_mediaimage(sender, instance, using, **kwargs):
    delete_version_image(instance)


class MediaFile(Media):
    file = models.FileField(
        _("file"), upload_to=file_upload_path,
        max_length=500, storage=MB_STORAGE
    )

    def __init__(self, *args, **kwargs):
        super(MediaFile, self).__init__(*args, **kwargs)
        self.prev_file_name = self.file.name if self.file else ''
        self.prev_published = self.published

    def save(self, *args, **kwargs):
        if self.file:
            if self.file.name != self.prev_file_name:
                self.extension = self.file.name.split('.')[-1]
            if not self.name:
                self.name = self.file.name
        super(MediaFile, self).save(*args, **kwargs)

    @property
    def ext(self):
        return self.extension if self.extension else \
            self.file.name.split('.')[-1]

    def get_file_url(self):
        return reverse("mb-file", kwargs={"slug": self.slug, "ext": self.ext})


class NodePermission(models.Model):
    node = models.ForeignKey(
        "rest_mediabrowser.Node", related_name="nodes_through",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    permission = models.CharField(
        _("permission"), max_length=2, choices=PERMISSION_LEVELS)

    class Meta:
        unique_together = (("user", "node"),)

    def __str__(self):
        return f"{self.node} :: {self.user}"
