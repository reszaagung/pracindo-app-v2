import os
import logging
from django.conf import settings
from django.core.files import File
from django.db import transaction
from .models import StikerBesar, GenerateStikerBesar

logger = logging.getLogger(__name__)

def petakan_template(generate_obj: GenerateStikerBesar, jenis: str, pola: str):
    jenis_format = jenis.lower().replace(" ", "_")
    nama_file_target = f"stiker_{jenis_format}_{pola}.docx"
    
    template = StikerBesar.objects.filter(nama_file=nama_file_target, aktif=True).first()
    
    if not template:
        base_dir = str(settings.BASE_DIR)
        physical_path = os.path.join(base_dir, 'fitur', 'templates', jenis_format, nama_file_target)
        
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
            except Exception:
                return None
        else:
            return None

    with transaction.atomic():
        generate_obj.pola_terdeteksi = pola
        generate_obj.alamat_file = template
        generate_obj.save(update_fields=["pola_terdeteksi", "alamat_file"])
        
    return template