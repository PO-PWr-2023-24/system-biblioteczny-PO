from django import forms
from .models import Ksiazka
from .models import Uzytkownik


class RejestracjaUzytkownikaForm(forms.ModelForm):
    haslo = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Uzytkownik
        fields = ['email', 'imie', 'nazwisko', 'adres_zamieszkania', 'numer_telefonu', 'haslo']


class LogowanieForm(forms.Form):
    email = forms.EmailField()
    haslo = forms.CharField(widget=forms.PasswordInput())


class RezerwacjaForm(forms.Form):
    ksiazka_id = forms.ModelChoiceField(queryset=Ksiazka.objects.filter(dostepnosc=True), empty_label="Wybierz książkę",
                                        label="Książka")


class WypozyczenieOnlineForm(forms.Form):
    ksiazka_id = forms.ModelChoiceField(queryset=Ksiazka.objects.filter(dostepnosc=True), empty_label="Wybierz książkę",
                                        label="Książka")
