from django.db import models

from core.models import DiauditModel


class BaseFinanceModel(DiauditModel):
    """Semua model finance: dibuat_pada / diubah_pada / dibuat_oleh dari
    core.DiauditModel, plus is_active untuk arsip tanpa hapus baris."""

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True