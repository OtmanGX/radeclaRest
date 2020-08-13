import threading
import time
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from core.task import SerialThread

# if SerialThread.start is True:
#     for t in threading.enumerate():
#         if t.name == 'serialThread':
#             print('thread found')
#             thread = t
# else:
#     thread = SerialThread()
#     print(thread)
#     thread.start()


class Terrain(models.Model):
    matricule = models.SmallIntegerField(blank=False)


class Reservation(models.Model):
    terrain = models.ForeignKey(Terrain, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    nom1 = models.CharField(max_length=30, blank=False)
    prenom1 = models.CharField(max_length=20, blank=False)
    nom2 = models.CharField(max_length=30, blank=True)
    prenom2 = models.CharField(max_length=20, blank=True)
    nom3 = models.CharField(max_length=30, blank=False)
    prenom3 = models.CharField(max_length=20, blank=False)
    nom4 = models.CharField(max_length=30, blank=True)
    prenom4 = models.CharField(max_length=20, blank=True)
    eclairage = models.BooleanField(default=False, blank=False)
    eclairage_paye = models.BooleanField(default=False, blank=False)
    entrainement = models.BooleanField(default=False, blank=False)


def get_day_reservations():
    now = timezone.now()
    return Reservation.objects.filter(terrain__id=1, start_date__year=now.year,
                                      start_date__month=now.month, start_date__day=now.day)


@receiver(models.signals.post_delete, sender=Reservation)
@receiver(models.signals.post_save, sender=Reservation)
def send_to_serial(sender, instance, **kwargs):
    print('receiver called')
    thread = None
    if SerialThread.begin:
        for t in threading.enumerate():
            if t.name == 'serialThread':
                print('thread found')
                thread = t
    tram1 = ['0']*16
    tram2 = ['0']*16
    for res in get_day_reservations():
        print(res.start_date)
        hour = res.start_date.hour-7
        tram1[hour] = '1'
        if res.eclairage_paye:
            tram2[hour] = '1'
    print('20;'+';'.join(tram1))
    if thread is not None:
        thread.send(bytes('20;'+';'.join(tram1)))
        time.sleep(2)
        thread.send(bytes(';'.join(tram2)))
