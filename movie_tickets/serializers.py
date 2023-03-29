from rest_framework import serializers
from .models import Movie, Showtime, Ticket

class MovieSerializer(serializers.ModelSerializer):
    showtimes = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'showtimes')

    def get_showtimes(self, obj):
        # Return a list of showtimes for the movie
        return Showtime.objects.filter(movie=obj).values_list('id', flat=True)


class ShowtimeSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()
    tickets_sold = serializers.SerializerMethodField()
    available_seats = serializers.ReadOnlyField()

    class Meta:
        model = Showtime
        fields = ('id', 'movie', 'time', 'tickets_sold', 'available_seats')

    def get_tickets_sold(self, obj):
        # Return the number of tickets sold for the showtime
        return sum(ticket.quantity for ticket in Ticket.objects.filter(showtime=obj))


class TicketSerializer(serializers.ModelSerializer):
    showtime = serializers.StringRelatedField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'showtime', 'quantity')

    def validate(self, attrs, *args, **kwargs):
        showtime = kwargs['showtime']
        quantity = args['quantity']
        if showtime.available_seats < quantity:
            raise serializers.ValidationError('Not enough available seats')
        return attrs

    def create(self, validated_data):
        showtime = validated_data['showtime']
        quantity = validated_data['quantity']
        if showtime.available_seats < quantity:
            raise serializers.ValidationError('Not enough available seats')
        showtime.available_seats -= quantity
        showtime.save()
        return super().create(validated_data)
