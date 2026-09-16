from django.conf import settings
from django.db import models


class BaseFinanceModel(models.Model):
    """Base abstract field set untuk semua model di app finance."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True