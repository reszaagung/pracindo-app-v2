from django.db import migrations

def buat_satuan_default(apps, schema_editor):
    Satuan = apps.get_model('master', 'Satuan')
    
    satuan_awal = [
        {'kode': 'KG', 'nama': 'Kilogram'},
        {'kode': 'G' , 'nama': 'Gram' },
        {'kode': 'PCS', 'nama': 'Pieces'},
        {'kode': 'LTR', 'nama': 'Liter'},
        {'kode': 'SAK', 'nama': 'Sak / Karung'},
        {'kode': 'TON', 'nama': 'Ton'},
        {'kode': 'M', 'nama': 'Meter'},
        {'kode': 'DRUM', 'nama': 'Drum'},
    ]
    
    for item in satuan_awal:
        Satuan.objects.get_or_create(kode=item['kode'], defaults={'nama': item['nama']})

def hapus_satuan_default(apps, schema_editor):
    Satuan = apps.get_model('master', 'Satuan')
    Satuan.objects.filter(kode__in=['KG', 'G', 'PCS', 'LTR', 'SAK', 'TON', 'M', 'DRUM']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(buat_satuan_default, hapus_satuan_default),
    ]