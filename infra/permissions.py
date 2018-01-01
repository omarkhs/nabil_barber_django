from rest_framework import permissions

#TODO: this will modified in the future for admins/barbers
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
            return obj == request.user

