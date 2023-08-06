from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass


@admin.register(MediaImage)
class MediaImageAdmin(admin.ModelAdmin):
    pass


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    pass


@admin.register(NodePermission)
class NodePermissionAdmin(admin.ModelAdmin):
    pass
