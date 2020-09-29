from core.models import *
from django.db.models import Value, When, Case

Reservation.objects.update(type_match=Case(When(entrainement=True, then=Value("E")), default=Value("M")))
