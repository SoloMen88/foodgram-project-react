from rest_framework import permissions


class AuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method == 'GET' or request.user.is_authenticated)
