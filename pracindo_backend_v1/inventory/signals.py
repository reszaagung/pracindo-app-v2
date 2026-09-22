from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.models import Entitas

from .models import Packing, SaldoEntitas


def pastikan_saldo_entitas(entitas):
    """
    Memastikan setiap Entitas memiliki satu SaldoEntitas.
    Aman dipanggil berkali-kali karena menggunakan get_or_create().
    """
    saldo, created = SaldoEntitas.objects.get_or_create(
        entitas=entitas
    )

    return saldo, created


@receiver(
    post_save,
    sender=Entitas,
)
def buat_saldo_entitas(
    sender,
    instance,
    created,
    **kwargs,
):
    if created:
        pastikan_saldo_entitas(instance)


@receiver(
    post_save,
    sender=Packing,
)
def eksekusi_posting_packing(
    sender,
    instance,
    created,
    **kwargs,
):
    pass


@receiver(
    post_delete,
    sender=Packing,
)
def rollback_stok_packing_terhapus(
    sender,
    instance,
    **kwargs,
):
    pass