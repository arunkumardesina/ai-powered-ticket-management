from rest_framework.permissions import BasePermission


class IsRole(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in self.allowed_roles)


class IsCustomer(IsRole):
    allowed_roles = ("CUSTOMER",)


class IsAgent(IsRole):
    allowed_roles = ("AGENT",)


class IsAdministrator(IsRole):
    allowed_roles = ("ADMIN",)


class IsAgentOrAdministrator(IsRole):
    allowed_roles = ("AGENT", "ADMIN")
