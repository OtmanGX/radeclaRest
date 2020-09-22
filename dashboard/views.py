from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Time
from datetime import datetime, timedelta

# Query
from django.db.models.functions import Coalesce
from django.db.models import Sum, Count, F, Q, Avg
from django.db.models.functions import ExtractHour, ExtractDay
from core.models import Terrain, Membre, Reservation

time_to_zero = lambda d: \
    d.replace(hour=0, minute=0, second=0, microsecond=0)


def current_month():
    d = time_to_zero(datetime.utcnow())
    return d.replace(day=1)


def current_week():
    d = time_to_zero(datetime.utcnow())
    return d - timedelta(d.weekday())


def current_day():
    d = time_to_zero(datetime.utcnow())
    return d


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def dashboard_view(request):
    terrain_month = Terrain.objects.annotate(
        heures=Coalesce(Sum('reservations__duration', filter=Q(reservations__start_date__gte=current_month())),
                        0)).order_by('-heures').values('matricule', 'heures')
    terrain_week = Terrain.objects.annotate(
        heures=Coalesce(Sum('reservations__duration', filter=Q(reservations__start_date__gte=current_week())),
                        0)).order_by('matricule').values('matricule', 'heures')
    terrain_day = Terrain.objects.annotate(
        heures=Coalesce(Sum('reservations__duration', filter=Q(reservations__start_date__gte=current_day())),
                        0)).order_by('matricule').values('matricule', 'heures')

    entraineur_month = Membre.objects.filter(entraineur=True).annotate(
        total=Count('reservations', filter=Q(reservations__start_date__gte=current_month()))).values("nom", "total")
    entraineur_week = Membre.objects.filter(entraineur=True).annotate(
        total=Count('reservations', filter=Q(reservations__start_date__gte=current_week()))).values("nom", "total")
    entraineur_day = Membre.objects.filter(entraineur=True).annotate(
        total=Count('reservations', filter=Q(reservations__start_date__gte=current_day()))).values("nom", "total")

    hours = Reservation.objects.annotate(hour=ExtractHour('start_date')).values('hour').annotate(
        nb=Count('hour')).order_by('-nb')[:5]

    moyen = Reservation.objects.annotate(day=ExtractDay('start_date')).values('day').annotate(
        total_duration=Sum('duration')).aggregate(avg_hours=Avg('total_duration'))
    moyen['avg_hours'] = round(moyen['avg_hours'], 1)

    nmembres = Membre.objects.filter(entraineur=False).exclude(cotisation=None).count()
    nentraineurs = Membre.objects.exclude(entraineur=False).count()
    nexternes = Membre.objects.filter(cotisation=None, entraineur=False).count()

    return Response({'terrainMonth': terrain_month,
                     'terrainWeek': terrain_week,
                     'terrainDay': terrain_day,
                     'entraineur': [entraineur_month, entraineur_week, entraineur_day],
                     'hours': hours,
                     'avg_hours': moyen['avg_hours'],
                     'nmembres': nmembres,
                     'nentraineurs': nentraineurs,
                     'nexternes': nexternes
                     })


@api_view(['GET'])
def terrain_stats(request):
    _date = request.GET.get("date")
    _year = request.GET.get("year")
    _month = request.GET.get("month")
    _year2 = request.GET.get("year")
    _month2 = request.GET.get("month")

    if _date == 'month':
        if _year2:
            terrain_month = Terrain.objects.annotate(
                heures=Coalesce(Sum('reservations__duration',
                                    filter=Q(reservations__start_date__year__range=(_year, _year2)) & Q(reservations__start_date__month__range=(_month, _month2))
                                           & Q(reservations__entrainement=False)
                                    ), 0),
                heures2=Coalesce(Sum('reservations__duration',
                                        filter=Q(reservations__start_date__year__range=(_year, _year2)) & Q(reservations__start_date__month__range=(_month, _month2))
                                     & Q(reservations__entrainement=True)
                                        ), 0),

            ).order_by('-heures').values(
                'matricule', 'heures', 'heures2')
        terrain_month = Terrain.objects.annotate(
            heures=Coalesce(Sum('reservations__duration',
                                filter=Q(reservations__start_date__year=_year) & Q(reservations__start_date__month=_month) & Q(reservations__entrainement=False)), 0),
            heures2=Coalesce(Sum('reservations__duration',
                                 filter=Q(reservations__start_date__year=_year) & Q(reservations__start_date__month=_month)
                                        & Q(reservations__entrainement=True)
                                 ), 0),
        ).order_by('-heures').values('matricule', 'heures', 'heures2')
        return Response(terrain_month)

    return Response({})


