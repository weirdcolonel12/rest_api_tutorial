from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    """
    custom permission to only owners of an object to edit it
    """


    def has_object_permission(self, request, view, obj):

        # read permissions are allowed to all User

        if request.method in permissions.SAFE_METHODS:
            return True

        # write permission is allowed to only user

        return obj.owner == request.user
