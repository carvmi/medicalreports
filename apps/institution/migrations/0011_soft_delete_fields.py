from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("institution", "0010_alter_institution_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="address",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="institution",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="institution",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
