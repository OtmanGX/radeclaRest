from django.apps import AppConfig
# Query
from django.db.models.functions import Coalesce
from django.db.models import Sum, Count, F, Q, Avg
from django.db.models.functions import ExtractHour, ExtractDay
from core.models import Terrain, Membre, Reservation


class DashboardConfig(AppConfig):
    name = 'dashboard'





def get_terrain_month(_year, _year2, _month, _month2):
    if _year2:
        terrain_month = Terrain.objects.annotate(
            heures=Coalesce(Sum('reservations__duration',
                                filter=Q(reservations__start_date__year__range=(_year, _year2)) & Q(
                                    reservations__start_date__month__range=(_month, _month2))
                                       & Q(reservations__type_match='M')
                                ), 0),
            heures2=Coalesce(Sum('reservations__duration',
                                 filter=Q(reservations__start_date__year__range=(_year, _year2)) & Q(
                                     reservations__start_date__month__range=(_month, _month2))
                                        & Q(reservations__type_match='E')
                                 ), 0),

        ).order_by('matricule').values(
            'matricule', 'heures', 'heures2')
    else:
        terrain_month = Terrain.objects.annotate(
            heures=Coalesce(Sum('reservations__duration',
                                filter=Q(reservations__start_date__year=_year) & Q(
                                    reservations__start_date__month=_month) & Q(reservations__type_match='M')), 0),
            heures2=Coalesce(Sum('reservations__duration',
                                 filter=Q(reservations__start_date__year=_year) & Q(
                                     reservations__start_date__month=_month)
                                        & Q(reservations__type_match='E')
                                 ), 0),
        ).order_by('matricule').values('matricule', 'heures', 'heures2')
    return terrain_month


def get_terrain_week(_year, _year2, _week, _week2):
    if _year2:
        res = Terrain.objects.annotate(
            heures=Coalesce(Sum('reservations__duration',
                                filter=Q(reservations__start_date__year__range=(_year, _year2)) & Q(
                                    reservations__start_date__week__range=(_week, _week2))
                                       & Q(reservations__type_match='M')
                                ), 0),
            heures2=Coalesce(Sum('reservations__duration',
                                 filter=Q(reservations__start_date__year__range=(_year, _year2)) & Q(
                                     reservations__start_date__week__range=(_week, _week2))
                                        & Q(reservations__type_match='E')
                                 ), 0),

        ).order_by('matricule').values(
            'matricule', 'heures', 'heures2')
    else:
        res = Terrain.objects.annotate(
            heures=Coalesce(Sum('reservations__duration',
                                filter=Q(reservations__start_date__year=_year) & Q(
                                    reservations__start_date__week=_week) & Q(reservations__type_match='M')), 0),
            heures2=Coalesce(Sum('reservations__duration',
                                 filter=Q(reservations__start_date__year=_year) & Q(
                                     reservations__start_date__week=_week)
                                        & Q(reservations__type_match='E')
                                 ), 0),
        ).order_by('matricule').values('matricule', 'heures', 'heures2')
    return res


def get_terrain_day(_year, _month, _day):
    res = Terrain.objects.annotate(
        heures=Coalesce(Sum('reservations__duration',
                            filter=Q(reservations__start_date__year=_year) &
                                   Q(reservations__start_date__month=_month) &
                                   Q(reservations__start_date__day=_day)
                                   & Q(reservations__type_match='M')), 0),
        heures2=Coalesce(Sum('reservations__duration',
                             filter=Q(reservations__start_date__year=_year) &
                                    Q(reservations__start_date__month=_month) &
                                    Q(reservations__start_date__day=_day) &
                                    Q(reservations__type_match='E')), 0)) \
        .order_by('-heures').values('matricule', 'heures', 'heures2')
    return res
