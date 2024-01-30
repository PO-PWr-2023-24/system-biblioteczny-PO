# Generated by Django 5.0.1 on 2024-01-24 10:54

import biblioteka_app.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("biblioteka_app", "0003_remove_wypozyczenie_pozycja_ksiazka_autor_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wypozyczenie",
            name="dataWypozyczenia",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="wypozyczenie",
            name="dataZwrotu",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="wypozyczenie",
            name="deadline",
            field=models.DateTimeField(default=biblioteka_app.models.oblicz_deadline),
        ),
    ]