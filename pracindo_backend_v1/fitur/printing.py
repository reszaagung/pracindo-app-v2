import logging
from pathlib import Path
from django.conf import settings
from docxtpl import DocxTemplate

logger = logging.getLogger(__name__)

def format_desimal(nilai):
    teks = f"{nilai:.2f}".rstrip("0").rstrip(".")
    return teks or "0"

def susun_konteks(generate_obj):
    # ...tidak berubah, tetap sama seperti sebelumnya...
    urutan_grup = list(generate_obj.pola_terdeteksi)
    item_per_grup = {item.grup: item for item in generate_obj.item_set.all()}
    konteks = {}
    for slot_ke in range(1, 5):
        if slot_ke <= len(urutan_grup):
            grup = urutan_grup[slot_ke - 1]
            item = item_per_grup[grup]
            konteks[f"slot{slot_ke}_nama"] = item.nama_item
            konteks[f"slot{slot_ke}_tipe"] = item.tipe
            konteks[f"slot{slot_ke}_lot"] = item.lot.strftime("%d%m%Y")
            konteks[f"slot{slot_ke}_net"] = format_desimal(item.net)
        else:
            konteks[f"slot{slot_ke}_nama"] = " "
            konteks[f"slot{slot_ke}_tipe"] = " "
            konteks[f"slot{slot_ke}_lot"] = " "
            konteks[f"slot{slot_ke}_net"] = " "
    return konteks

def generate_docx_saja(generate_obj, folder_output=None):
    """Hanya membuat file .docx dan menyimpannya ke folder output."""
    if generate_obj.alamat_file is None:
        raise ValueError("Template belum terpasang.")

    if folder_output is None:
        folder_output = Path(settings.MEDIA_ROOT) / "output_stiker"

    Path(folder_output).mkdir(parents=True, exist_ok=True)
    path_output = Path(folder_output) / f"Stiker_{generate_obj.pk}_{generate_obj.pola_terdeteksi}.docx"

    tpl = DocxTemplate(generate_obj.alamat_file.file_template.path)
    tpl.render(susun_konteks(generate_obj))
    tpl.save(str(path_output))

    generate_obj.file_hasil = str(path_output)
    generate_obj.save()

    return path_output