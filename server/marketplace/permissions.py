from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

class IsContractor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            hasattr(request.user, "profile") and request.user.profile.role == "CONTRACTOR"
        )

class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and hasattr(request.user, "profile")):
            return False
        return request.user.profile.role in ("ADMIN", "MODERATOR") or request.user.is_staff
