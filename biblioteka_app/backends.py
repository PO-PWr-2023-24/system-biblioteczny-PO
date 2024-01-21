from django.contrib.auth.backends import ModelBackend
from .models import Uzytkownik

class UzytkownikBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            uzytkownik = Uzytkownik.objects.get(email=email)
            if uzytkownik.check_password(password):
                return uzytkownik
        except Uzytkownik.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Uzytkownik.objects.get(pk=user_id)
        except Uzytkownik.DoesNotExist:
            return None
