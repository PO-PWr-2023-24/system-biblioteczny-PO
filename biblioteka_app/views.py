from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .backends import UzytkownikBackend
from .forms import LogowanieForm
from .forms import RejestracjaUzytkownikaForm
from .forms import RezerwacjaForm
from .forms import WypozyczenieOnlineForm
from .models import Czytelnik, Kara, Wypozyczenie
from .models import Rezerwacja, Ksiazka, StatusWypozyczenia
from .serializers import BookSerializer, BookUpdateSerializer

NOT_AUTHENTICATED = 0


class LoginView(APIView):
    # Log in to the system.
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({'error': 'Nieprawidłowe dane uwierzytelniające'}, status=status.HTTP_401_UNAUTHORIZED)


class BooksView(APIView):
    permission_classes = [IsAuthenticated]

    # Get a list of all books.
    def get(self, request):
        books = Ksiazka.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookView(APIView):
    permission_classes = [IsAuthenticated]

    # Get a details of the book.
    def get(self, request, id):
        book = get_object_or_404(Ksiazka, pk=id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    # Update the details of a book
    def put(self, request, id):
        book = get_object_or_404(Ksiazka, pk=id)
        serializer = BookUpdateSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            updated_serializer = BookSerializer(book)
            return Response(updated_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReserveBookView(APIView):
    permission_classes = [IsAuthenticated]

    # This endpoint reserve the selected book.
    def post(self, request, id):
        user = request.user
        book = get_object_or_404(Ksiazka, pk=id)
        czytelnik = get_object_or_404(Czytelnik, uzytkownik=user)
        if book.dostepnosc and not book.czy_online:
            Rezerwacja.objects.create(
                czytelnik=czytelnik,
                ksiazka=book,
                dataRezerwacji=timezone.now()
            )
            book.dostepnosc = False
            book.save()
            return JsonResponse({"message": "Book reserved successfully"}, status=200)
        else:
            return JsonResponse({"message": "Can't reserve book"}, status=409)

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


def lista_ksiazek(request):
    if request.method == 'GET':
        ksiazki = Ksiazka.objects.all()
        data = [
            {
                'book_id': ksiazka.id,
                'title': ksiazka.tytul,
                'author': ksiazka.autor,
                'form': ksiazka.forma.nazwa,
                'availability': True if ksiazka.dostepnosc else False
            }
            for ksiazka in ksiazki
        ]
        return JsonResponse(data, safe=False)


def wypozyczenia_czytelnika(request, user_id):
    if request.method == 'GET':
        czytelnik = Czytelnik.objects.get(uzytkownik__id=user_id)
        wypozyczenia = Wypozyczenie.objects.filter(czytelnik=czytelnik).select_related('ksiazka', 'status')
        data = [
            {
                'loan_id': w.id,
                'start_date': w.dataWypozyczenia,
                'end_date': w.dataZwrotu,
                'deadline': w.deadline,
                'status': w.status.nazwa,
                'reader_id': user_id,
                'book_id': w.ksiazka.id,
                'book_info': f"{w.ksiazka.tytul}, {w.ksiazka.autor}"
            } for w in wypozyczenia
        ]
        return JsonResponse(data, safe=False)


@require_http_methods(["POST"])
def rent_online(request, book_id):
    user = request.user
    book = get_object_or_404(Ksiazka, pk=book_id)
    czytelnik = get_object_or_404(Czytelnik, uzytkownik=user)
    status, created = StatusWypozyczenia.objects.get_or_create(nazwa="wypożyczona")
    if book.dostepnosc and book.forma.nazwa == 'digital':
        wypozyczenie = Wypozyczenie.objects.create(
            czytelnik=czytelnik,
            ksiazka=book,
            status=status
        )
        # book.dostepnosc = False
        book.save()
        return JsonResponse({"message": "Książka wypożyczona pomyślnie."}, status=200)
    else:
        return JsonResponse({"message": "Książka nie jest dostępna."}, status=400)


@require_http_methods(["POST"])
def make_reservation(request, book_id):
    user = request.user
    book = get_object_or_404(Ksiazka, pk=book_id)
    czytelnik = get_object_or_404(Czytelnik, uzytkownik=user)

    if book.dostepnosc and book.forma.nazwa == 'paper':
        Rezerwacja.objects.create(
            czytelnik=czytelnik,
            ksiazka=book,
            dataRezerwacji=timezone.now()
        )
        book.dostepnosc = False
        book.save()
        return JsonResponse({"message": "Rezerwacja dokonana pomyślnie."}, status=200)
    else:
        return JsonResponse({"message": "Książka nie jest dostępna."}, status=400)
