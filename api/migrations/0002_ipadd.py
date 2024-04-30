# Generated by Django 4.2.5 on 2024-04-30 17:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="IpAdd",
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
                ("ipAddr", models.CharField(default="", max_length=20)),
                ("time", models.DateTimeField(default=datetime.datetime.now)),
                ("os", models.CharField(default="", max_length=30)),
                ("browser", models.CharField(default="", max_length=30)),
                ("device", models.CharField(default="", max_length=30)),
            ],
        ),
    ]
