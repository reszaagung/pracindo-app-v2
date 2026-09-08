from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from akunting.services_import import import_po_massal


class Command(BaseCommand):
    help = "Import massal Purchase Order dari file Excel."

    def add_arguments(self, parser):
        parser.add_argument('file_excel', type=str)
        parser.add_argument('--user', type=str, required=True, help='Username untuk field dibuat_oleh')

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            user = User.objects.get(username=options['user'])
        except User.DoesNotExist:
            raise CommandError(f"User '{options['user']}' tidak ditemukan.")

        path = options['file_excel']
        try:
            with open(path, 'rb') as f:
                hasil = import_po_massal(f, user=user)
        except FileNotFoundError:
            raise CommandError(f"File tidak ditemukan: {path}")

        for item in hasil['berhasil']:
            self.stdout.write(self.style.SUCCESS(f"[OK] {item['grup']} -> {item['no_po']} (id={item['id']})"))
        for item in hasil['gagal']:
            self.stdout.write(self.style.ERROR(f"[GAGAL] {item['grup']}: {item['pesan']}"))

        self.stdout.write(f"\nTotal: {len(hasil['berhasil'])} berhasil, {len(hasil['gagal'])} gagal.")