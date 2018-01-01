from rest_framework import permissions

#TODO: this will modified in the future for admins/barbers
class UserPermissions(permissions.BasePermission):
    def has_permission( self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update']:
            return obj == request.user

        return True
