from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0003_alter_sex"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="patient",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
