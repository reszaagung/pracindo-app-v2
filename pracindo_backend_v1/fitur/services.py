import logging
from django.db import transaction
from .models import StikerBesar, GenerateStikerBesar

logger = logging.getLogger(__name__)

def petakan_template(generate_obj: GenerateStikerBesar, jenis: str, pola: str):
    nama_file_target = f"stiker_{jenis}_{pola}.docx"
    
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