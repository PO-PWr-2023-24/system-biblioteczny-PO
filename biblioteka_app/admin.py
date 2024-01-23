from django.contrib import admin
from .models import Uzytkownik, Adres, Pracownik, Czytelnik, Katalog
from .models import Gatunek, FormaKsiazki, StatusWypozyczenia, StatusKary
from .models import Ksiazka, Wypozyczenie, Rezerwacja, Kara

# Rejestracja modeli
admin.site.register(Uzytkownik)
admin.site.register(Adres)
admin.site.register(Pracownik)
admin.site.register(Czytelnik)
admin.site.register(Katalog)
admin.site.register(Gatunek)
admin.site.register(FormaKsiazki)
admin.site.register(StatusWypozyczenia)
admin.site.register(StatusKary)
admin.site.register(Ksiazka)
admin.site.register(Wypozyczenie)
admin.site.register(Rezerwacja)
admin.site.register(Kara)
