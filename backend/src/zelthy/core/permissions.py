from rest_framework.permissions import IsAuthenticated
from .common_utils import get_client_ip


class CheckIPWhitelisting:
    def check_ipwhitelisting(self, request):
        if not request.tenant.whitelist_ips:
            return True
        client_ip = get_client_ip(request)

        whitelisted = request.tenant.whitelist_ips.split(",")
        whitelisted = [w.strip() for w in whitelisted]
        if client_ip in whitelisted:
            return True
        return False


class IsAuthenticatedPlatformUser(IsAuthenticated, CheckIPWhitelisting):
    def has_permission(self, request, view):
        if not self.check_ipwhitelisting(request):
            return False
        if super(IsAuthenticatedPlatformUser, self).has_permission(request, view):
            try:
                platform_user = request.user.platform_user
                if (
                    platform_user.__class__.__name__ == "PlatformUserModel"
                    and platform_user.is_active
                ):
                    return True
            except:
                return False
        return False


class IsAuthenticatedAppUser(IsAuthenticated, CheckIPWhitelisting):
    def has_permission(self, request, view):
        if super(IsAuthenticatedAppUser, self).has_permission(request, view):
            try:
                app_user = request.user.app_user
                if app_user.__class__.__name__ == "AppUserModel" and app_user.is_active:
                    return True
            except:
                return False
        return False
