from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from .models import Uzytkownik, Ksiazka, Czytelnik, Wypozyczenie, Rezerwacja, FormaKsiazki, Gatunek, StatusWypozyczenia


class BookRentalAndReservationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Uzytkownik.objects.create_user('test@example.com', 'testpassword')
        self.client.login(email='test@example.com', password='testpassword')

        # Tworzenie instancji FormaKsiazki
        forma_digital = FormaKsiazki.objects.create(nazwa="digital")
        forma_paper = FormaKsiazki.objects.create(nazwa="paper")

        gatunek = Gatunek.objects.create(nazwa="Fantastyka")
        status_wypozyczenia = StatusWypozyczenia.objects.create(nazwa="wypożyczona")


        # Teraz używamy instancji FormaKsiazki zamiast ciągu znaków
        self.book_digital = Ksiazka.objects.create(
            autor="Autor 1", tytul="Książka Cyfrowa", forma=forma_digital,gatunek=gatunek, dostepnosc=True)
        self.book_paper = Ksiazka.objects.create(
            autor="Autor 2", tytul="Książka Papierowa", forma=forma_paper,gatunek=gatunek, dostepnosc=True)

        self.czytelnik = Czytelnik.objects.create(uzytkownik=self.user)

    def test_rent_online(self):
        response = self.client.post(reverse('rent_online', args=[self.book_digital.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Wypozyczenie.objects.count(), 1)

    def test_make_reservation(self):
        response = self.client.post(reverse('make_reservation', args=[self.book_paper.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rezerwacja.objects.count(), 1)
