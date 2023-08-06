from rest_framework.permissions import BasePermission
from rest_framework import exceptions

class CrudPermissions(BasePermission):
    #copied from DjangoModelPermissions

    # Map methods into required permission codes.
    # Override this if you need to also provide 'view' permissions,
    # or if you want to provide custom permission codes.
    message = "Permission Denined"
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'], #permission changed
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    action_map = {'list','create','retrieve','update','partial_update','destroy'}
    authenticated_users_only = True

    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """

        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }
        
        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    def _queryset(self, view):
        assert hasattr(view, 'get_queryset') \
            or getattr(view, 'queryset', None) is not None, (
            'Cannot apply {} on a view that does not set '
            '`.queryset` or have a `.get_queryset()` method.'
        ).format(self.__class__.__name__)

        if hasattr(view, 'get_queryset'):
            queryset = view.get_queryset()
            assert queryset is not None, (
                '{}.get_queryset() returned None'.format(view.__class__.__name__)
            )
            return queryset
        return view.queryset

    def has_permission(self, request, view):
        if view.action not in self.action_map :
            return True
        else:
            if getattr(view, '_ignore_model_permissions', False):
                return True

            if not request.user or (
            not request.user.is_authenticated and self.authenticated_users_only):
                return False
            queryset = self._queryset(view)
            perms = self.get_required_permissions(request.method, queryset.model)
        return request.user.has_perms(perms)
        
