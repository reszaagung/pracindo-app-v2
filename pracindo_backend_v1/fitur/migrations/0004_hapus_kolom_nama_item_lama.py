from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitur', '0003_alter_itemcetakkecil12_nama_item'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE fitur_itemcetak DROP COLUMN IF EXISTS nama_item;',
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
