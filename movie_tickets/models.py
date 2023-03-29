from django.db import models
import uuid
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from django.db import models

class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    genre = models.TextField(default="Horror")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie-detail', args=[str(self.id)])

class Showtime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.DateTimeField()
    available_seats = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f'{self.movie.title} at {self.time}'

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    email = models.EmailField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)
