from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import login
from .backends import UzytkownikBackend
from django.shortcuts import render, redirect
from .forms import RejestracjaUzytkownikaForm
from django.contrib.auth.hashers import make_password
from .forms import LogowanieForm
from django.utils import timezone
from datetime import timedelta
from .models import Rezerwacja, Ksiazka
from .forms import RezerwacjaForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from .models import Czytelnik, Kara, Wypozyczenie
from .forms import WypozyczenieOnlineForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

NOT_AUTHENTICATED = 0


def rejestracja(request):
    if request.method == 'POST':
        form = RejestracjaUzytkownikaForm(request.POST)
        if form.is_valid():
            uzytkownik = form.save(commit=False)
            uzytkownik.haslo = make_password(form.cleaned_data['haslo'])
            uzytkownik.save()
            Czytelnik.objects.create(uzytkownik=uzytkownik)
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

    # return render(request, 'logowanie.html', {'form': form})
    return JsonResponse({"ala": "Ma kota"})

@login_required
def rezerwuj_ksiazke(request):
    form = RezerwacjaForm()
    if request.method == 'POST':
        form = RezerwacjaForm(request.POST)
        if form.is_valid():
            ksiazka = form.cleaned_data['ksiazka_id']
            if ksiazka.dostepnosc:
                try:
                    czytelnik = Czytelnik.objects.get(uzytkownik=request.user)
                except Czytelnik.DoesNotExist:
                    return render(request, 'error.html', {'message': 'Tylko czytelnicy mogą rezerwować książki.'})
                Rezerwacja.objects.create(
                    czytelnik=czytelnik,
                    ksiazka=ksiazka,
                    dataRezerwacji=timezone.now()
                )
                ksiazka.dostepnosc = False  # Oznacz książkę jako niedostępną
                ksiazka.save()
                # przekieruj do strony potwierdzenia lub wyświetl komunikat o sukcesie
                return redirect('jakas_strona')
    # return render(request, 'rezerwacja.html', {'form': form})
    return '{"aa":2}'


@login_required
def wypozycz_ksiazke_online(request):
    form = WypozyczenieOnlineForm()
    if request.method == 'POST':
        form = WypozyczenieOnlineForm(request.POST)
        if form.is_valid():
            ksiazka = form.cleaned_data['ksiazka_id']
           # czytelnik = Czytelnik.objects.get(uzytkownik=request.user.czytelnik)

            # Sprawdzenie, czy czytelnik ma nieopłacone kary
            try:
                czytelnik = Czytelnik.objects.get(uzytkownik=request.user)
            except Czytelnik.DoesNotExist:
                return render(request, 'error.html', {'message': 'Tylko czytelnicy mogą wypożyczać książki online.'})

            if Kara.objects.filter(czytelnik=czytelnik, status='nieopłacona').exists():
                return render(request, 'error.html', {'message': 'Posiadasz nieopłaconą karę.'})

            # Logika wypożyczenia online
            Wypozyczenie.objects.create(
                czytelnik=czytelnik,
                pozycja=ksiazka,
                dataWypozyczenia=timezone.now(),
                deadline=timezone.now() + timedelta(days=14),  # Przykładowy termin zwrotu
                status='wypożyczona'
            )
            return redirect('moje_konto')

    return render(request, 'wypozycz_online.html', {'form': form})