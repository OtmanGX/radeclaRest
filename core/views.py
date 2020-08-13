from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import Reservation
from core.serializers import ReservationSerializer


class HelloView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'username': 'admin'}
        return Response(content)


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['terrain__matricule', ]

    def list(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date', None)
        if start_date:
            end_date = request.GET.get('end_date')
            queryset = Reservation.objects.filter(start_date__range=(start_date, end_date))
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return super().list(self, request, *args, **kwargs)
