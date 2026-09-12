from rest_framework import permissions
from staff_user.models import Role

def adalah_kurir(user):
    return getattr(user, 'role', None) == Role.KURIR and not user.is_superuser

def batasi_ke_kurir(qs, user, lewat='kurir_id'):
    if not adalah_kurir(user):
        return qs
    return qs.filter(**{lewat: user.id})

class KurirTidakMengubahRute(permissions.BasePermission):
    message = 'Kurir tidak berwenang mengubah susunan pengiriman.'
    AKSI_KURIR = {
        'list', 'retrieve', 'sampai', 'bukti', 'retur', 
        'tugas_saya', 'berangkatkan', 'kolam_tugas', 'klaim'
    }

    def has_permission(self, request, view):
        if not adalah_kurir(request.user):
            return True
        return getattr(view, 'action', None) in self.AKSI_KURIR

class HanyaKurirPengiriman(permissions.BasePermission):
    message = 'Anda bukan kurir pengiriman ini.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or getattr(request.user, 'supervisor', False):
            return True
        kurir_id = getattr(obj, 'kurir_id', None)
        if kurir_id is None:
            kurir_id = getattr(getattr(obj, 'pengiriman', None), 'kurir_id', None)
        if kurir_id is None:
            return True
        if adalah_kurir(request.user):
            return kurir_id == request.user.id
        return True