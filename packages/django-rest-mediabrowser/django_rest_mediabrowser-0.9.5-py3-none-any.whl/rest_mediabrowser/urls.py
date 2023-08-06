from django.urls import path, include
# from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from . import views as mv_views

router = DefaultRouter()

router.register(r'collections', mv_views.CollectionViewSet)
router.register(r'shared/collections', mv_views.SharedCollectionViewSet,
                basename='shared-collection')
# router.register(r'images', MediaImageViewSet)
# router.register(r'files', MediaFileViewSet)
router.register("media", mv_views.MediaViewSet, basename="media")
# router.register(r'shared/images', SharedMediaImageViewSet,
#                 basename='shared-images')
# router.register(r'shared/files', SharedMediaFileViewSet,
#                 basename='shared-file')
router.register(r'shared/media', mv_views.SharedMediaViewSet,
                basename='shared-media')
router.register(r'permission', mv_views.NodePermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # re_path(r'^(?P<path>.*)$', MediaFilesView.as_view(),
    #           name='serve_private_file'),

    path('images/<str:slug>/file.<str:ext>',
         mv_views.MediaStorageImageView.as_view(), name='mb-image'),
    path('images/<str:slug>/versions/<str:version>/file.<str:ext>',
         mv_views.MediaStorageImageVersionView.as_view(), name='mb-version'),
    path('images/<str:slug>/thumbnail.<str:ext>',
         mv_views.MediaStorageImageThumbnailView.as_view(),
         name='mb-thumbnail'),
    path('files/<str:slug>/file.<str:ext>',
         mv_views.MediaStorageFileView.as_view(), name='mb-file'),
]
