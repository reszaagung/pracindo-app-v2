import logging
import string
from pathlib import Path
from django.conf import settings
from docxtpl import DocxTemplate

logger = logging.getLogger(__name__)

def format_desimal(nilai):
    teks = f"{nilai:.2f}".rstrip("0").rstrip(".")
    return teks or "0"

def _ambil_nama_tampil(nama_item):
    """nama_item bisa teks polos (ItemCetak besar, tidak diubah) atau
    instance MasterProduk (ItemCetakKecil12, via FK). Disamakan jadi
    string di sini, supaya susun_konteks tetap satu fungsi buat
    besar+kecil12."""
    if hasattr(nama_item, "nama_item"):  # dikonfirmasi dari search_fields MasterProdukViewSet
        return nama_item.nama_item
    return nama_item

HURUF_KE_SLOT = {huruf: i + 1 for i, huruf in enumerate(string.ascii_uppercase[:12])}

def susun_konteks(generate_obj, jumlah_slot=4):
    item_per_grup = {item.grup: item for item in generate_obj.item_set.all()}
    konteks = {}

    for slot_ke in range(1, jumlah_slot + 1):
        konteks[f"slot{slot_ke}_nama"] = " "
        konteks[f"slot{slot_ke}_tipe"] = " "
        konteks[f"slot{slot_ke}_lot"] = " "
        konteks[f"slot{slot_ke}_net"] = " "

    for grup, item in item_per_grup.items():
        slot_ke = HURUF_KE_SLOT.get(grup)
        if slot_ke is None or slot_ke > jumlah_slot:
            logger.warning("Grup di luar jangkauan slot (jumlah_slot=%s): %r", jumlah_slot, grup)
            continue
        konteks[f"slot{slot_ke}_nama"] = _ambil_nama_tampil(item.nama_item)
        konteks[f"slot{slot_ke}_tipe"] = item.tipe
        konteks[f"slot{slot_ke}_lot"] = item.lot.strftime("%d%m%Y")
        konteks[f"slot{slot_ke}_net"] = format_desimal(item.net)

    return konteks

def generate_docx_saja(generate_obj, folder_output=None, jumlah_slot=4):
    if generate_obj.alamat_file is None:
        raise ValueError("Template belum terpasang.")

    if folder_output is None:
        folder_output = Path(settings.MEDIA_ROOT) / "output_stiker"

    Path(folder_output).mkdir(parents=True, exist_ok=True)
    path_output = Path(folder_output) / f"Stiker_{generate_obj.pk}_{generate_obj.pola_terdeteksi}.docx"

    tpl = DocxTemplate(generate_obj.alamat_file.file_template.path)
    tpl.render(susun_konteks(generate_obj, jumlah_slot=jumlah_slot))
    tpl.save(str(path_output))

    generate_obj.file_hasil = str(path_output)
    generate_obj.save()

    return path_output