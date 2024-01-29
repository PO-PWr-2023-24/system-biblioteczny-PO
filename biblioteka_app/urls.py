from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('books', views.BooksView.as_view(), name='books'),
    path('book/<int:id>', views.BookView.as_view(), name='book'),
    path('reservation/<int:id>/', views.ReserveBookView.as_view(), name='reserve_book'),
    path('reservations/', views.UserReservationsView.as_view(), name='reservation_list'),
]
