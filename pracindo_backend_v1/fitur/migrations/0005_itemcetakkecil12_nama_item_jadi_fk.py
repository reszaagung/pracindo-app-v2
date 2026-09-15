from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitur', '0004_hapus_kolom_nama_item_lama'),
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemcetakkecil12',
            name='nama_item',
        ),
        migrations.AddField(
            model_name='itemcetakkecil12',
            name='nama_item',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='packing_hasil_kecil12',
                to='master.masterproduk',
                null=True,
            ),
            preserve_default=False,
        ),
    ]
