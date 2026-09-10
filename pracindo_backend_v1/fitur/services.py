import os
import logging
from django.conf import settings
from django.core.files import File
from django.db import transaction
from .models import StikerBesar, GenerateStikerBesar

logger = logging.getLogger(__name__)

def petakan_template(generate_obj: GenerateStikerBesar, jenis: str, pola: str):
    nama_file_target = f"stiker_{jenis}_{pola}.docx"
    
    try:
        template = StikerBesar.objects.get(nama_file=nama_file_target, aktif=True)
    except StikerBesar.DoesNotExist:
        physical_path = os.path.join(settings.BASE_DIR, 'fitur', 'templates', jenis, nama_file_target)
        
        if os.path.exists(physical_path):
            try:
                with open(physical_path, 'rb') as f:
                    django_file = File(f, name=nama_file_target)
                    template, _ = StikerBesar.objects.update_or_create(
                        nama_file=nama_file_target,
                        defaults={
                            'file_template': django_file,
                            'aktif': True
                        }
                    )
                logger.info("Template '%s' otomatis didaftarkan ke database dari direktori fisik.", nama_file_target)
            except Exception as e:
                logger.error("Gagal mendaftarkan file fisik '%s': %s", nama_file_target, e)
                return None
        else:
            logger.error("Template '%s' tidak ditemukan di Master Data maupun folder fisik: %s", nama_file_target, physical_path)
            return None

    with transaction.atomic():
        generate_obj.pola_terdeteksi = pola
        generate_obj.alamat_file = template
        generate_obj.save(update_fields=["pola_terdeteksi", "alamat_file"])
        
    return template