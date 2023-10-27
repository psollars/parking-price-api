# Generated by Django 4.2.6 on 2023-10-24 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Rate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("days", models.TextField()),
                ("times", models.TextField()),
                ("tz", models.TextField()),
                ("price", models.IntegerField()),
            ],
        ),
    ]