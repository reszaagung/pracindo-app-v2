from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import Entitas
from .models import SaldoEntitas, Packing

@receiver(post_save, sender=Entitas)
def buat_saldo_entitas(sender, instance, created, **kwargs):
    if created:
        SaldoEntitas.objects.get_or_create(entitas=instance)

@receiver(post_save, sender=Packing)
def eksekusi_posting_packing(sender, instance, created, **kwargs):
    # Dikosongkan total karena sudah diurus services.py
    pass

@receiver(post_delete, sender=Packing)
def rollback_stok_packing_terhapus(sender, instance, **kwargs):
    # Dikosongkan total karena sudah diurus services.py
    pass