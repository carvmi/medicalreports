from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("medprofiles", "0002_remove_healthprofessional_institution_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="healthprofessional",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="healthprofessional",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
