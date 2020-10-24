from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Time
from datetime import datetime, timedelta
# Query
from django.db.models.functions import Coalesce
from django.db.models import Sum, Count, F, Q, Avg
from django.db.models.functions import ExtractHour, ExtractDay

from config.apps import read_config
from core.models import Terrain, Membre, Reservation, Cotisation
from dashboard.apps import get_terrain_month, get_terrain_week, get_terrain_day

from core.models import *
import csv

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


def export_membres_toexcel(request):
    membres = Membre.objects.distinct().annotate(
        montant_cotisation=F('cotisation__montant'),
        cotisation_montant_payé=F('cotisation__montant_paye'),
        cotisation_date_paiement=F('cotisation__created_at'), ).distinct() \
        .values('id', 'nom', 'sexe', 'mail', 'tel', 'age', 'date_naissance',
                'profession',
                'tournoi', 'licence_féderation', 'cotisation__type', 'cotisation__paye',
                'montant_cotisation', 'cotisation_montant_payé', 'cotisation_date_paiement')
    for m in membres:
        if m['cotisation_date_paiement']:
            m['cotisation_date_paiement'] = m['cotisation_date_paiement'].date()
    with open('file.csv', 'w') as csvfile:
        fieldnames = list(membres[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        writer.writerows(membres)
    # sending response
    f = open('file.csv', 'r')
    response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="membres.xls"'
    return response


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
    _year2 = request.GET.get("year2")
    _month2 = request.GET.get("month2")
    _week = request.GET.get("week")
    _week2 = request.GET.get("week2")
    _day = request.GET.get("day")

    if _date == 'month':
        terrain_month = get_terrain_month(_year, _year2, _month, _month2)
        return Response(terrain_month)
    elif _date == 'week':
        terrain_week = get_terrain_week(_year, _year2, _week, _week2)
        return Response(terrain_week)
    elif _date == 'day':
        terrain_day = get_terrain_day(_year, _month, _day)
        return Response(terrain_day)

    return Response({})


@api_view(['GET'])
def top_hours_stats(request):
    hours = Reservation.objects.annotate(hour=ExtractHour('start_date')).values('hour').annotate(
        nb=Count('hour')).order_by('-nb')[:5]
    by_age = request.GET.get('age')
    if by_age:
        age_ranges = ([5, 10], [10, 12], [12, 16], [18, 25],
                      [25, 40], [40, 50], [50, 60], [60, 70], [70, 80])
        res = {}
        for age_range in age_ranges:
            res['-'.join(map(str, age_range))] = {hour: Reservation.objects.filter(players__age__range=age_range,
                                                                                   start_date__hour=hour).count() for
                                                  hour in map(lambda x: x['hour'], hours[::-1])}
        return Response(res)

    return Response(hours)


@api_view(['GET'])
def training_stats(request):
    _date = request.GET.get("date")
    _year = request.GET.get("year")
    _month = request.GET.get("month")
    _year2 = request.GET.get("year2")
    _month2 = request.GET.get("month2")
    _week = request.GET.get("week")
    _week2 = request.GET.get("week2")
    _day = request.GET.get("day")
    _membre = request.GET.get("with")

    myfilter = Q(reservations__start_date__year=_year)
    if _date == 'month':
        myfilter = myfilter & Q(reservations__start_date__month=_month)
    elif _date == 'week':
        myfilter = myfilter & Q(reservations__start_date__week=_week)
    if _membre:
        myfilter = myfilter & Q(reservations__players__nom=_membre)

    res = Membre.objects.filter(entraineur=True).annotate(
        total=Coalesce(Sum('reservations__duration', filter=myfilter), 0)).order_by('-total').values("nom", "total")
    res2 = {}
    if _membre is None:
        for elem in res:
            res2[elem['nom']] = Membre.objects.filter(myfilter, entraineur=False,
                                                      reservations__players__nom=elem['nom']).annotate(
                total=Coalesce(Sum('reservations__duration'),
                               0)).order_by('-total').values("nom", "total")

    return Response({'training': res,
                     'members': res2})


@api_view(['GET'])
def lighting_stats(request):
    _date = request.GET.get("date")
    _year = request.GET.get("year")
    _month = request.GET.get("month")
    _day = request.GET.get("day")

    myfilter = Q(reservations__eclairage_paye=True, reservations__start_date__year=_year)
    if _date == 'month':
        myfilter = myfilter & Q(reservations__start_date__month=_month)
    elif _date == 'day':
        myfilter = myfilter & Q(reservations__start_date__day=_day, reservations__start_date__month=_month)

    res = Terrain.objects.annotate(
        heures=Coalesce(Sum('reservations__duration',
                            filter=myfilter), 0))

    return Response(res.values('matricule', 'heures'))


@api_view(['GET'])
def terrain_stats_hours(request):
    _date = request.GET.get("date")
    _year = request.GET.get("year")
    _month = request.GET.get("month")
    _year2 = request.GET.get("year2")
    _month2 = request.GET.get("month2")
    _week = request.GET.get("week")
    _week2 = request.GET.get("week2")
    _day = request.GET.get("day")
    myfilter = Q(reservations__start_date__year=_year)
    total_days = 365
    if _date == 'month':
        myfilter = myfilter & Q(reservations__start_date__month=_month)
        total_days = 30
    elif _date == 'week':
        myfilter = myfilter & Q(reservations__start_date__week=_week)
        total_days = 7
    elif _date == 'day':
        myfilter = myfilter & Q(reservations__start_date__month=_month, reservations__start_date__day=_day)
        total_days = 1

    res1 = Terrain.objects.filter(myfilter,
                                  reservations__start_date__hour__range=[7, 12]).aggregate(
        total=Coalesce(Sum('reservations__duration'), 0)).get('total')

    res2 = Terrain.objects.filter(myfilter,
                                  reservations__start_date__hour__range=[13, 17]).aggregate(
        total=Coalesce(Sum('reservations__duration'), 0)).get('total')

    res3 = Terrain.objects.filter(myfilter,
                                  reservations__start_date__hour__range=[18, 23]).aggregate(
        total=Coalesce(Sum('reservations__duration'), 0)).get('total')

    return Response({
        'h8_14': round(res1 * 100 / (54 * total_days), 2),
        'h14_19': round(res2 * 100 / (45 * total_days), 2),
        'h19_24': round(res3 * 100 / (45 * total_days), 2)})


@api_view(['GET'])
def total_cotisation(request):
    res = Cotisation.objects.filter(created_at__year=2020).aggregate(total=Sum('montant_paye'))
    return Response(res)


@api_view(['GET'])
def cotisation_a_payer(request):
    res = Cotisation.objects.filter(created_at__year=2020).aggregate(total=(Sum('montant') - Sum('montant_paye')))
    return Response(res)


@api_view(['GET'])
def members_stats(request):
    _date = request.GET.get("date")
    _year = request.GET.get("year")
    _month = request.GET.get("month")
    _year2 = request.GET.get("year2")
    _month2 = request.GET.get("month2")
    _week = request.GET.get("week")
    _week2 = request.GET.get("week2")
    _day = request.GET.get("day")
    _membre = request.GET.get("with")
    myfilter = Q(reservations__start_date__year=_year)
    if _date == 'month':
        myfilter = myfilter & Q(reservations__start_date__month=_month)
    elif _date == 'week':
        myfilter = myfilter & Q(reservations__start_date__week=_week)
    if _membre:
        myfilter = myfilter & Q(reservations__players__nom=_membre)

    myfilter2 = myfilter & Q(reservations__type_match='M')
    myfilter3 = myfilter & Q(reservations__type_match='E')
    res = Membre.objects.filter(entraineur=False).annotate(
        total=Coalesce(Sum('reservations__duration', filter=myfilter), 0),
        match=Coalesce(Sum('reservations__duration', filter=myfilter2), 0),
        entrainement=Coalesce(Sum('reservations__duration', filter=myfilter3), 0), ).order_by('-total').values("nom",
                                                                                                               "match",
                                                                                                               "entrainement",
                                                                                                               "total")
    return Response(res)


@api_view(['GET'])
def main_stats(request):
    now = timezone.now()
    res1 = Terrain.objects.filter(reservations__start_date__day=now.day,
                                  reservations__start_date__month=now.month,
                                  reservations__start_date__hour__range=[7, 12]).count()

    res2 = Terrain.objects.filter(reservations__start_date__day=now.day,
                                  reservations__start_date__month=now.month,
                                  reservations__start_date__hour__range=[13, 17]).count()

    res3 = Terrain.objects.filter(reservations__start_date__day=now.day,
                                  reservations__start_date__month=now.month,
                                  reservations__start_date__hour__range=[18, 23]).count()

    membres = Membre.objects.filter(entraineur=False).count()
    membres_paye = Membre.objects.filter(cotisation__paye=True).count()

    res = Reservation.objects.filter(start_date__year=now.year,
                                     start_date__month=now.month,
                                     start_date__day=now.day)

    lighting_count = Reservation.objects.filter(start_date__day=now.day,
                                                start_date__month=now.month,
                                                start_date__year=now.year,
                                                eclairage_paye=True).count()

    config = read_config()
    lighting_hour = config['rule4']['hour']
    entrainement = res.filter(type_match='E')
    match = res.filter(type_match='M')
    tournoi = res.filter(type_match='T')
    defi = res.filter(type_match='D')
    birth_day = Membre.objects.filter(date_naissance__month=now.month, date_naissance__day=now.day)

    return Response({
        'h8_14': round(res1 * 100 / 54, 2),
        'h14_19': round(res2 * 100 / 45, 2),
        'h19_24': round(res3 * 100 / 45, 2),
        'total_membres': membres,
        'membres_paye': membres_paye,
        'entrainement': entrainement.count(),
        'match': match.count(),
        'tournoi': tournoi.count(),
        'defi': defi.count(),
        'lighting_count': lighting_count,
        'lighting_hour': lighting_hour,
        'birth_day': ', '.join([i.nom for i in birth_day]) if birth_day.count() else False
    })
