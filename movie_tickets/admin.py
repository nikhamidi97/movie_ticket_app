from django.contrib import admin
from .models import Movie, Showtime, Ticket

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre']

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['id','movie', 'time']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id','get_movie', 'email', 'quantity']

    @admin.display(ordering='movie__title', description='Showtime')
    def get_movie(self, obj):
        return f'{obj.showtime.movie.title} at ({obj.showtime.time})'
