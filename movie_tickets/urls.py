# movie_tickets/urls.py

from django.urls import path
from .views import MovieViewSet, ShowtimeViewSet, TicketViewSet,TicketCreate

urlpatterns = [
    path('movies/', MovieViewSet.as_view(), name='movie-list'),
    path('movies/<str:movie_id>/', MovieViewSet.as_view(), name='movie-detail'),
    path('movies/<str:movie_id>/showtimes/', ShowtimeViewSet.as_view(), name='showtime-list'),
    path('showtimes/<str:showtime_id>/', ShowtimeViewSet.as_view(), name='showtime-detail'),
    path('showtimes/<str:showtime_id>/purchase/', TicketViewSet.as_view(), name='ticket-purchase'),
    path('tickets/create/', TicketCreate.as_view(), name='ticket-create'),
]
