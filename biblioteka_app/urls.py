from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('books', views.BooksView.as_view(), name='books'),
    path('book/<int:id>', views.BookView.as_view(), name='book'),
]
