from rest_framework import permissions

USER_ACTIONS_ALLOW_ANY = ['list', 'retrieve', 'create']


class UsersPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in USER_ACTIONS_ALLOW_ANY:
            return True
        if view.action == 'me':
            return request.user.is_authenticated
        return True
