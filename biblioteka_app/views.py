from django.shortcuts import render
from django.contrib.auth import login
from .backends import UzytkownikBackend
from django.shortcuts import render, redirect
from .forms import RejestracjaUzytkownikaForm
from django.contrib.auth.hashers import make_password
from .forms import LogowanieForm

NOT_AUTHENTICATED = 0


def rejestracja(request):
    if request.method == 'POST':
        form = RejestracjaUzytkownikaForm(request.POST)
        if form.is_valid():
            uzytkownik = form.save(commit=False)
            uzytkownik.haslo = make_password(form.cleaned_data['haslo'])
            uzytkownik.save()
            # Tutaj możesz dodać logikę tworzenia obiektu Czytelnik
            return redirect('login')  # Przekieruj do strony logowania po pomyślnej rejestracji
    else:
        form = RejestracjaUzytkownikaForm()

    return render(request, 'rejestracja.html', {'form': form})


def logowanie(request):
    if request.method == 'POST':
        form = LogowanieForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            haslo = form.cleaned_data['haslo']
            uzytkownik = UzytkownikBackend().authenticate(request, email=email, haslo=haslo)
            if uzytkownik is not None:
                login(request, uzytkownik)
                return redirect('strona_glowna')  # Przekieruj do strony głównej po zalogowaniu
            else:
                return NOT_AUTHENTICATED
    else:
        form = LogowanieForm()

    return render(request, 'logowanie.html', {'form': form})
