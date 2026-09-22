from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0007_alter_kemasan_options_alter_packing_options_and_more"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="packing",
            name="ix_pack_batch_baru",
        ),
        migrations.RemoveField(
            model_name="packing",
            name="batch",
        ),
        migrations.AddField(
            model_name="packing",
            name="tangki",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="packing_set",
                to="produksi.tangki",
            ),
        ),
        migrations.AddIndex(
            model_name="packing",
            index=models.Index(
                fields=["tangki", "status"],
                name="ix_pack_tangki_baru",
            ),
        ),
    ]
