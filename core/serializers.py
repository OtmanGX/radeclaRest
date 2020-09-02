from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.fields import empty

from core.models import Reservation, Membre


class ReservationSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        if instance:
            if isinstance(instance, QuerySet):
                setattr(self.Meta, 'depth', 1)
            else:
                setattr(self.Meta, 'depth', 0)
        else:
            setattr(self.Meta, 'depth', 0)
        super(ReservationSerializer, self).__init__(instance, data, **kwargs)

    class Meta:
        model = Reservation
        fields = '__all__'
        depth = 0



class MembreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        fields = '__all__'
