from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
import threading
from core.task import SerialThread
from school.models import School


class Categorie(models.Model):
    nom = models.CharField(max_length=35, blank=False, unique=True)

    class Meta:
        ordering = ('nom',)

    def __str__(self):
        return self.nom


class Cotisation(models.Model):
    type = models.CharField(max_length=25, blank=False)
    paye = models.BooleanField(default=False)
    montant = models.PositiveSmallIntegerField(default=4000)
    montant_paye = models.PositiveSmallIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.type}"


class Membre(models.Model):
    SEX_CHOICES = (('H', 'HOMME'),
                   ('F', 'FEMME'))
    nom = models.CharField(max_length=35, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    sexe = models.CharField(choices=SEX_CHOICES, default='H', max_length=2)
    tel = models.CharField(max_length=13, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    age = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    mail = models.EmailField(blank=True, null=True)
    profession = models.CharField(max_length=35, null=True)
    entraineur = models.BooleanField(default=False)
    tournoi = models.BooleanField(default=False)
    licence_féderation = models.BooleanField(default=False)
    school = models.ForeignKey(School, blank=True, null=True, on_delete=models.CASCADE)
    categorie = models.ManyToManyField(Categorie, related_name="membres", blank=True)
    cotisation = models.ForeignKey(Cotisation, related_name='membres', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.nom


class Tournament(models.Model):
    name = models.CharField(max_length=50, blank=False)
    players = models.ManyToManyField(Membre, related_name='tournaments', blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    juges = models.TextField(blank=True)
    date = models.DateTimeField(blank=True, default=timezone.now())
    director = models.CharField(max_length=35, blank=True)
    type_tournoi = models.CharField(max_length=25, default='TCMT')
    # category = models.ForeignKey(Categorie, related_name='tournois', on_delete=models.CASCADE)
    trainers = models.TextField(blank=True)


class Terrain(models.Model):
    matricule = models.SmallIntegerField(blank=False)


class Reservation(models.Model):
    CHOICES = (
        ('E', 'Entrainement'),
        ('M', 'Match'),
        ('T', 'Tournoi'),
        ('D', 'Défi'),
    )
    terrain = models.ForeignKey(Terrain, related_name='reservations', on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    duration = models.PositiveSmallIntegerField(default=1)
    end_date = models.DateTimeField(blank=True, null=True)
    players = models.ManyToManyField(Membre, related_name='reservations', blank=True)
    tournoi = models.ForeignKey(Tournament, related_name='matchs', on_delete=models.CASCADE, blank=True, null=True)
    eclairage = models.BooleanField(default=False, blank=False)
    eclairage_paye = models.BooleanField(default=False, blank=False)
    entrainement = models.BooleanField(default=False, blank=False)
    type_match = models.CharField(choices=CHOICES, default='M', max_length=25)

    class Meta:
        ordering = ['-start_date']


def get_day_reservations():
    now = timezone.now()
    return Reservation.objects.filter(terrain__id=1, start_date__year=now.year,
                                      start_date__month=now.month, start_date__day=now.day)


def signal():
    thread = None
    if SerialThread.begin:
        for t in threading.enumerate():
            if t.name == 'serialThread':
                print('thread found')
                thread = t
    tram1 = ['0'] * 16
    tram2 = ['0'] * 16
    for res in get_day_reservations():
        print(res.start_date)
        hour = res.start_date.hour - 7
        tram1[hour] = '1'
        if res.eclairage_paye:
            tram2[hour] = '1'

    if thread is not None:
        thread.msg = (bytes('20;' + ';'.join(tram1) + ';', encoding="utf-8"),
                      bytes(';'.join(tram2), encoding="utf-8"))


@receiver(models.signals.post_save, sender=Reservation)
def send_to_serial(sender, instance, **kwargs):
    print('receiver called')
    # signal()
    threading.Thread(target=signal).start()


@receiver(models.signals.post_delete, sender=Reservation)
def send_to_serial2(sender, instance, **kwargs):
    print('receiver delete called')
    # signal()
    threading.Thread(target=signal).start()
