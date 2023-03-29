# movie_tickets/views.py

from rest_framework import generics
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Showtime, Ticket
from .serializers import MovieSerializer, ShowtimeSerializer, TicketSerializer


class MovieViewSet(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']

    def get_queryset(self):
        return Movie.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get(self, request, *args, **kwargs):
        if 'movie_id' in self.kwargs:
            try:
                obj = self.queryset.get(id=self.kwargs['movie_id'])
                serializer = self.get_serializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Movie.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ShowtimeViewSet(generics.ListAPIView):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['time']

    def get_queryset(self):
        return Showtime.objects.all()

    def get(self, request, *args, **kwargs):

            try:
                if 'showtime_id' in self.kwargs:
                    obj = self.queryset.get(id=self.kwargs['showtime_id'])
                else:
                    movie= Movie.objects.get(id=self.kwargs['movie_id'])
                    obj = self.queryset.filter(movie=movie)
                    if obj.exists():
                        serializer = self.get_serializer(obj, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_404_NOT_FOUND)
            except Showtime.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketViewSet(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        showtime_id = kwargs['showtime_id']
        showtime= Showtime.objects.get(id=showtime_id)
        data = {
            'showtime': showtime,
            'user': request.user,
            'quantity': request.data.get('quantity')
        }
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@method_decorator(name='create', decorator=swagger_auto_schema(request_body=TicketSerializer))
class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated)
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.delete()

    @swagger_auto_schema(
        operation_summary="Create a ticket",
        operation_description="Create a new ticket with the given quantity.",
        request_body=TicketSerializer,
        responses={
            201: TicketSerializer(),
            400: "Invalid input data",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class TicketCreate(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Send email confirmation to the user
        ticket = serializer.save()

    def get_queryset(self):
        # Only show showtimes that haven't started yet
        return Showtime.objects.filter(time__gt=timezone.now())

    def get_serializer_context(self):
        # Pass the request to the serializer context
        return {'request': self.request}
