from rest_framework import permissions


class IsAdminAndCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        return obj.added_by == request.user and request.user.is_superuser
