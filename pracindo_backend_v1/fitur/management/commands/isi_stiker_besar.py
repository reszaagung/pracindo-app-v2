# myapp/management/commands/isi_master_stiker_besar.py  (tidak berubah dari sebelumnya)
from django.core.management.base import BaseCommand
from myapp.models import StikerBesar

POLA = ["AAAA", "AAAB", "AABB", "AABC", "ABBB", "ABBC", "ABCC", "ABCD"]
JENIS = ["polos", "cv"]


class Command(BaseCommand):
    help = "Mengisi master data StikerBesar untuk semua kombinasi jenis x pola"

    def handle(self, *args, **kwargs):
        for jenis in JENIS:
            for pola in POLA:
                nama_file = f"stiker_{jenis}_besar_{pola}"
                _, dibuat = StikerBesar.objects.get_or_create(nama_file=nama_file)
                self.stdout.write(f"{nama_file}: {'dibuat' if dibuat else 'sudah ada'}")