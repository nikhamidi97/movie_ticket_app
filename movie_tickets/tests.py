from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Movie, Showtime, Ticket
import uuid
from datetime import datetime, timedelta
from django.contrib.auth.models import User



class MovieTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='admin', password='admin')
        self.client = Client()
        self.client.login(username='admin', password='admin')
        self.movie_data = {
            'title': 'The Shining',
            'genre': 'Horror'
        }

    def test_create_movie(self):
        response = self.client.post(reverse('movie-list'), self.movie_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.movie_data['title'])


class ShowtimeTestCase(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title='The Shining', genre='Horror')
        self.showtime_data = {
            'id': str(uuid.uuid4()),
            'movie': self.movie,
            'time': datetime.now() + timedelta(hours=1),
            'available_seats': 20
        }

    def test_create_showtime(self):
        showtime = Showtime.objects.create(**self.showtime_data)
        self.assertEqual(showtime.movie, self.movie)

    def test_retrieve_showtime_tickets(self):
        showtime = Showtime.objects.create(movie=self.movie, time=datetime.now() + timedelta(hours=1), available_seats=20)
        ticket_data = {'showtime': showtime, 'email': 'test@example.com', 'quantity': 2}
        Ticket.objects.create(**ticket_data)
        url = reverse('showtime-detail', args=[showtime.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tickets_sold'], 2)


# class TicketTestCase(APITestCase):
#     def setUp(self):
#         self.movie = Movie.objects.create(title='The Shining', genre='Horror')
#         self.showtime = Showtime.objects.create(movie=self.movie, time=datetime.now() + timedelta(hours=1), available_seats=20)
#         self.ticket_data = {
#             'showtime': self.showtime.id,
#             'email': 'test@example.com',
#             'quantity': 2
#         }

#     def test_create_ticket(self):
#         url = reverse('ticket-list')
#         response = self.client.post(url, self.ticket_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['showtime'], 'The Shining at {}'.format(self.showtime.time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')))
#         self.assertEqual(self.showtime.available_seats, 18)

#     def test_create_ticket_insufficient_seats(self):
#         self.showtime.available_seats = 1
#         self.showtime.save()
#         url = reverse('ticket-list')
#         response = self.client.post(url, self.ticket_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['detail'], 'Not enough available seats')
