# retail/permissions.py
from rest_framework.permissions import BasePermission

class IsMasterUser(BasePermission):
    """Master = user yang TIDAK terhubung ke CabangToko manapun —
    pola yang sama persis dipakai get_user_cabang() di views.py lain."""
    message = "Hanya akun master yang bisa membuat cabang baru."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and not hasattr(request.user, "cabang_toko")
        )