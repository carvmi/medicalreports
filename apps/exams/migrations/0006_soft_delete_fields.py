from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exams", "0005_alter_mammogramexam_image_alter_mammogramexam_itype_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="mammogramexam",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="mammogramexam",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
