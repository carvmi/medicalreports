from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_remove_patient_rg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='sex',
            new_name='gender',
        ),
    ]
