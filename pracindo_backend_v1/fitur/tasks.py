from celery import shared_task
import logging
from .models import GenerateStikerBesar
from .printing import generate_docx_saja

logger = logging.getLogger(__name__)

@shared_task
def task_generate_stiker(generate_id):
    try:
        obj = GenerateStikerBesar.objects.get(pk=generate_id)

        path_file = generate_docx_saja(obj)
        logger.info(f"Berhasil generate: {path_file}")

        obj.file_hasil = str(path_file)
        obj.save(update_fields=["file_hasil"])

    except GenerateStikerBesar.DoesNotExist:
        logger.error(f"ID {generate_id} tidak ditemukan.")
    except Exception as e:
        logger.error(f"Gagal generate stiker ID {generate_id}: {e}")