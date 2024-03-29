# Generated by Django 5.0.1 on 2024-01-22 18:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("biblioteka_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Czytelnik",
            fields=[
                (
                    "uzytkownik",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FormaKsiazki",
            fields=[
                (
                    "nazwa",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Gatunek",
            fields=[
                (
                    "nazwa",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pracownik",
            fields=[
                (
                    "uzytkownik",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StatusKary",
            fields=[
                (
                    "nazwa",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StatusWypozyczenia",
            fields=[
                (
                    "nazwa",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ksiazka",
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
                ("dostepnosc", models.BooleanField()),
                (
                    "forma",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.formaksiazki",
                    ),
                ),
                (
                    "gatunek",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.gatunek",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pozycja",
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
                ("autor", models.CharField(max_length=100)),
                ("tytul", models.CharField(max_length=100)),
                (
                    "ksiazka",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.ksiazka",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Katalog",
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
                (
                    "pracownik",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.pracownik",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rezerwacja",
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
                ("dataRezerwacji", models.DateTimeField()),
                (
                    "czytelnik",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.czytelnik",
                    ),
                ),
                (
                    "ksiazka",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.ksiazka",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Kara",
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
                ("wartosc", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "czytelnik",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.czytelnik",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.statuskary",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Wypozyczenie",
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
                ("dataWypozyczenia", models.DateTimeField()),
                ("dataZwrotu", models.DateTimeField()),
                ("deadline", models.DateTimeField()),
                (
                    "czytelnik",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.czytelnik",
                    ),
                ),
                (
                    "pozycja",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.pozycja",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="biblioteka_app.statuswypozyczenia",
                    ),
                ),
            ],
        ),
    ]
