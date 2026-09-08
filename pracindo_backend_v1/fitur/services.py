# services.py
import logging
from django.db import transaction
from .models import StikerBesar, GenerateStikerBesar

logger = logging.getLogger(__name__)
PREFIX = {"polos": "stiker_polos_besar", "cv": "stiker_cv_besar"}


def petakan_template(generate_obj: GenerateStikerBesar, jenis: str, pola: str):
    nama_file_target = f"{PREFIX.get(jenis, 'stiker_polos_besar')}_{pola}"
    try:
        template = StikerBesar.objects.get(nama_file=nama_file_target, aktif=True)
    except StikerBesar.DoesNotExist:
        logger.error("Template '%s' belum ada di Master Data.", nama_file_target)
        return None

    with transaction.atomic():
        generate_obj.pola_terdeteksi = pola
        generate_obj.alamat_file = template
        generate_obj.save(update_fields=["pola_terdeteksi", "alamat_file"])
    return template