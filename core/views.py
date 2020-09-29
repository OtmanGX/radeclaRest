import django_filters
from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from core.models import Reservation, Membre, Categorie, Cotisation
from core.serializers import ReservationSerializer, MembreSerializer, CategorieSerializer, CotisationSerializer, UserSerializer
from radeclaRest.utils import StandardResultsSetPagination

# Filter
# from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter

import logging

logger = logging.getLogger(__name__)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = UserSerializer(request.user)
        return Response(data=user.data)


class ReservationViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter, filters.BaseFilterBackend]
    search_fields = ['terrain__matricule', ]
    filter_fields = '__all__'

    def list(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date', None)
        if start_date:  
            end_date = request.GET.get('end_date')
            queryset = Reservation.objects.filter(start_date__range=(start_date, end_date))
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return super().list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class MembreFilter(django_filters.FilterSet):
    no_cotisation = django_filters.BooleanFilter(field_name='cotisation', lookup_expr='isnull')

    class Meta:
        model = Membre
        fields = ['nom', 'entraineur', 'cotisation', 'cotisation__paye', 'no_cotisation']


class MembreViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Membre.objects.all()
    serializer_class = MembreSerializer
    pagination_class = StandardResultsSetPagination
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter, filters.BaseFilterBackend]
    # no_cotisation = django_filters.BooleanFilter(name='cotisation__isnull')
    search_fields = ['nom', ]
    filterset_class = MembreFilter

    # filter_fields = ('nom', 'entraineur', 'cotisation', 'cotisation__paye', 'no_cotisation')

    def list(self, request, *args, **kwargs):
        is_all = request.GET.get('all', None)
        if is_all:
            queryset = Membre.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return super().list(self, request, *args, **kwargs)


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer


class CotisationViewSet(viewsets.ModelViewSet):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer
