from django.contrib.auth.models import AnonymousUser

from zelthy.apps.auditlogs.cid import set_cid
from zelthy.apps.auditlogs.context import set_actor
from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.shared.platformauth.models import PlatformUserModel
from zelthy.apps.dynamic_models.permissions import get_platform_user


class AuditlogMiddleware:
    """
    Middleware to couple the request's user to log items. This is accomplished by currying the
    signal receiver with the user from the request (or None if the user is not authenticated).
    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    @staticmethod
    def _get_remote_addr(request):
        # In case there is no proxy, return the original address
        if not request.headers.get("X-Forwarded-For"):
            return request.META.get("REMOTE_ADDR")

        # In case of proxy, set 'original' address
        remote_addr: str = request.headers.get("X-Forwarded-For").split(",")[0]

        # Remove port number from remote_addr
        if "." in remote_addr and ":" in remote_addr:  # IPv4 with port (`x.x.x.x:x`)
            remote_addr = remote_addr.split(":")[0]
        elif "[" in remote_addr:  # IPv6 with port (`[:::]:x`)
            remote_addr = remote_addr[1:].split("]")[0]

        return remote_addr

    @staticmethod
    def _get_actor(request):
        user = getattr(request, "user", None)
        if user is None or isinstance(user, AnonymousUser):
            platform_user = get_platform_user(request)
            if platform_user:
                user = platform_user
                return user
        if user.is_authenticated:
            return user
        return None

    def __call__(self, request):
        remote_addr = self._get_remote_addr(request)
        user = self._get_actor(request)
        set_cid(request)

        with set_actor(actor=user, remote_addr=remote_addr):
            return self.get_response(request)
