from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsMemberOrOrganization(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_verified and
            (request.user.user_type ==
             'MEMBER' or request.user.user_type == 'ORGANIZATION')
        )


class MemberAccessPermission(permissions.BasePermission):
    message = 'Adding Members not allowed.'

    def has_permission(self, request, view):
        ...
