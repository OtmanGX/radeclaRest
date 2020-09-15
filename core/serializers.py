from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.fields import empty

from core.models import Reservation, Membre, Categorie, Cotisation


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
    def __init__(self, instance=None, data=empty, **kwargs):
        if instance:
            # print(type(instance))
            # if isinstance(instance, QuerySet) or isinstance(instance, list):
            setattr(self.Meta, 'depth', 1)
            # else:
            #     setattr(self.Meta, 'depth', 0)
        else:
            setattr(self.Meta, 'depth', 0)
        super(MembreSerializer, self).__init__(instance, data, **kwargs)

    categorie = serializers.SlugRelatedField(many=True, queryset=Categorie.objects.all(), slug_field='nom',
                                             required=False)

    # cotisation = serializers.SlugRelatedField(queryset=Cotisation.objects.all(), slug_field='pk', required=False)

    class Meta:
        model = Membre
        fields = '__all__'
        depth = 0
        # fields = ('url', 'id', 'nom', 'sexe', 'tel', 'age', 'date_naissance', 'mail', 'date_naissance', 'entraineur',
        #           'licence_fideration', 'cotisation', 'categorie')


class CategorieSerializer(serializers.HyperlinkedModelSerializer):
    membres = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='membre-detail')

    class Meta:
        model = Categorie
        fields = ('nom', 'membres',)


class CotisationSerializer(serializers.ModelSerializer):
    # membres = MembreSerializer(many=True)
    membres = serializers.SlugRelatedField(many=True, queryset=Membre.objects.all(), slug_field='nom')

    class Meta:
        model = Cotisation
        fields = '__all__'
