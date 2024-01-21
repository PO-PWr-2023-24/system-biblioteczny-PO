from django import forms
from .models import Uzytkownik

class RejestracjaUzytkownikaForm(forms.ModelForm):
    haslo = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Uzytkownik
        fields = ['email', 'imie', 'nazwisko', 'adres_zamieszkania', 'numer_telefonu', 'haslo']

class LogowanieForm(forms.Form):
    email = forms.EmailField()
    haslo = forms.CharField(widget=forms.PasswordInput())
