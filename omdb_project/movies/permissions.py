from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    """Permission to update/delete record only for users who create it."""
    message = "Only user who created record can update/delete it"

    def has_object_permission(self, request, view, obj):
        if request.method in ('DELETE', 'PUT', 'PATCH'):
            return obj.user == request.user
        else:
            return True
