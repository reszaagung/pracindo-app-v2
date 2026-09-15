from django.db import migrations
from decimal import Decimal

def buat_kemasan_standar(apps, schema_editor):
    Kemasan = apps.get_model('inventory', 'Kemasan')
    
    daftar_template = [
        ("PCS@1KG", 1),
        ("GALON@5KG", 5),
        ("DUS@12KG", 12),
        ("PAIL@20KG", 20),
        ("PAIL@25KG", 25),
        ("PAIL@30KG", 30),
    ]
    
    for nama, bobot in daftar_template:
        Kemasan.objects.get_or_create(
            nama=nama, 
            defaults={"bobot_kg": Decimal(bobot), "aktif": True}
        )

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_stokbarangjadi_stokitemspabrik_and_more'), 
    ]

    operations = [
        migrations.RunPython(buat_kemasan_standar),
    ]
