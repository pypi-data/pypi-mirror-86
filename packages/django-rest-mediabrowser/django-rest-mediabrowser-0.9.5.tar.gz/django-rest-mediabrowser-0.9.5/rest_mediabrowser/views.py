from private_storage.views import PrivateStorageDetailView, PrivateStorageView
from django.utils.module_loading import import_string
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from . import appconfig
from . import models as mb_model
from . import serializers as mb_ser
from .permissions import NodePermission, IsNodePermissionOwner
from django_filters.rest_framework import DjangoFilterBackend

import logging
logger = logging.getLogger(__name__)


class MediaFilesView(PrivateStorageView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(
        appconfig.MEDIA_BROWSER_AUTH_FUNCTION))


class MediaStorageImageView(PrivateStorageDetailView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(
        appconfig.MEDIA_BROWSER_AUTH_FUNCTION))
    model = mb_model.MediaImage
    content_disposition = 'inline'
    model_file_field = 'image'
    lookup_field = "slug"


class MediaStorageImageVersionView(PrivateStorageDetailView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(
        appconfig.MEDIA_BROWSER_AUTH_FUNCTION))
    model = mb_model.MediaImage
    content_disposition = 'inline'
    model_file_field = 'image'
    lookup_field = "slug"

    def get_path(self):
        version = self.kwargs['version']
        # logger.critical(f"in view: {version}")
        if version == "original":
            file = getattr(self.object, self.model_file_field)
            return file.name
        version_image = self.object.get_version(version)
        return version_image


class MediaStorageImageThumbnailView(PrivateStorageDetailView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(
        appconfig.MEDIA_BROWSER_AUTH_FUNCTION))
    model = mb_model.MediaImage
    content_disposition = 'inline'
    model_file_field = 'thumbnail'
    lookup_field = "slug"


class MediaStorageFileView(PrivateStorageDetailView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(
        appconfig.MEDIA_BROWSER_AUTH_FUNCTION))
    model = mb_model.MediaFile
    content_disposition = 'inline'
    model_file_field = 'file'
    lookup_field = "slug"


class NodePermissionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsNodePermissionOwner)
    queryset = mb_model.NodePermission.objects.all()
    serializer_class = mb_ser.NodePermissionSerializer
    # lookup_field = "slug"

    def get_queryset(self):
        node_list = list(mb_model.Node.objects.filter(
            owner=self.request.user).values_list("id", flat=True))
        logger.critical(node_list)
        return mb_model.NodePermission.objects.filter(node__in=node_list)


class CollectionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, NodePermission, )
    queryset = mb_model.Collection.objects.all()
    serializer_class = mb_ser.CollectionSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return mb_model.Collection.objects.filter(owner=self.request.user)


class SharedCollectionViewSet(
        mixins.RetrieveModelMixin, mixins.ListModelMixin,
        viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, NodePermission, )
    queryset = mb_model.Collection.objects.all()
    serializer_class = mb_ser.SharedCollectionSerializer
    lookup_field = "slug"

    def get_queryset(self):
        if self.request.user:
            node_list = list(self.request.user.shared_nodes.all()
                             .values_list("id", flat=True))
            return mb_model.Collection.objects.filter(id__in=node_list)
        else:
            return mb_model.Collection.objects.none()


class MediaViewSet(viewsets.ModelViewSet):
    queryset = mb_model.Media.objects.all()
    serializer_class = mb_ser.MediaSerializer
    permission_classes = (IsAuthenticated, NodePermission, )
    lookup_field = "slug"

    def get_queryset(self):
        return mb_model.Media.objects.filter(owner=self.request.user)


class SharedMediaViewSet(
        mixins.RetrieveModelMixin, mixins.ListModelMixin,
        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = mb_model.Media.objects.all()
    serializer_class = mb_ser.SharedMediaSerializer
    permission_classes = (IsAuthenticated, NodePermission, )
    lookup_field = "slug"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('parent',)

    def get_queryset(self):
        if self.request.user:
            node_list = list(self.request.user.shared_nodes.all()
                             .values_list("id", flat=True))
            return mb_model.Media.objects.filter(id__in=node_list)
        else:
            return mb_model.Media.objects.none()
