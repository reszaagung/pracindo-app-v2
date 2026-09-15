from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitur', '0001_initial'),
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemcetak',
            name='nama_item',
        ),
        migrations.AddField(
            model_name='itemcetak',
            name='nama_item',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='packing_hasil_besar',
                to='master.masterproduk',
            ),
            preserve_default=False,
        ),
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
            ),
            preserve_default=False,
        ),
    ]
