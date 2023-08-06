from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)


class MediaBrowserBasePermission(permissions.BasePermission):
    field_name = None

    def has_object_permission(self, request, view, obj):
        # If user is the owner allow everything.
        # if obj.published and request.method in permissions.SAFE_METHODS:
        #     return True
        if obj.owner == request.user:
            return True
        perm = obj.shared_with.through.objects.filter(
            **{'user': request.user, self.field_name: obj})
        if not perm:
            # If no other permission return false
            return False
        else:
            perm_obj = perm[0]
            if perm_obj.permission == 'v':
                # Allow only to view
                if request.method in permissions.SAFE_METHODS:
                    return True
                else:
                    return False
            else:
                if request.method == 'DELETE':
                    return False
                else:
                    return True


class NodePermission(MediaBrowserBasePermission):
    field_name = 'node'


class IsNodePermissionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.node.owner
