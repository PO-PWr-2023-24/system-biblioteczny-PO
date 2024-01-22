from django.db import models
#
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models
from django.utils.translation import gettext_lazy as _
#
class UzytkownikManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Uzytkownik(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    imie = models.CharField(_('first name'), max_length=100)
    nazwisko = models.CharField(_('last name'), max_length=100)
    adres_zamieszkania = models.ForeignKey('Adres', on_delete=models.SET_NULL, null=True)
    numer_telefonu = models.CharField(max_length=15)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = UzytkownikManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['imie', 'nazwisko']

    def __str__(self):
        return self.email

class Adres(models.Model):
    ulica = models.CharField(max_length=100)
    nr_domu = models.CharField(max_length=10)
    nr_mieszkania = models.CharField(max_length=10)
    kod_pocztowy = models.CharField(max_length=10)
    miasto = models.CharField(max_length=100)


class Pracownik(models.Model):
    uzytkownik = models.OneToOneField(Uzytkownik, on_delete=models.CASCADE, primary_key=True)


class Czytelnik(models.Model):
    uzytkownik = models.OneToOneField(Uzytkownik, on_delete=models.CASCADE, primary_key=True)


class Katalog(models.Model):
    pracownik = models.ForeignKey(Pracownik, on_delete=models.CASCADE)


class Gatunek(models.Model):
    nazwa = models.CharField(max_length=100, primary_key=True)


class FormaKsiazki(models.Model):
    nazwa = models.CharField(max_length=100, primary_key=True)


class StatusWypozyczenia(models.Model):
    nazwa = models.CharField(max_length=100, primary_key=True)


class StatusKary(models.Model):
    nazwa = models.CharField(max_length=100, primary_key=True)


class Ksiazka(models.Model):
    forma = models.ForeignKey(FormaKsiazki, on_delete=models.CASCADE)
    dostepnosc = models.BooleanField()
    gatunek = models.ForeignKey(Gatunek, on_delete=models.CASCADE)


class Pozycja(models.Model):
    autor = models.CharField(max_length=100)
    tytul = models.CharField(max_length=100)
    ksiazka = models.ForeignKey(Ksiazka, on_delete=models.CASCADE)


class Wypozyczenie(models.Model):
    dataWypozyczenia = models.DateTimeField()
    dataZwrotu = models.DateTimeField()
    deadline = models.DateTimeField()
    status = models.ForeignKey(StatusWypozyczenia, on_delete=models.CASCADE)
    czytelnik = models.ForeignKey(Czytelnik, on_delete=models.CASCADE)
    pozycja = models.ForeignKey(Pozycja, on_delete=models.CASCADE)


class Rezerwacja(models.Model):
    czytelnik = models.ForeignKey(Czytelnik, on_delete=models.CASCADE)
    ksiazka = models.ForeignKey(Ksiazka, on_delete=models.CASCADE)
    dataRezerwacji = models.DateTimeField()


class Kara(models.Model):
    wartosc = models.DecimalField(max_digits=10, decimal_places=2)
    czytelnik = models.ForeignKey(Czytelnik, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusKary, on_delete=models.CASCADE)
