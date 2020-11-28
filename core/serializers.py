from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.fields import empty

from config.apps import read_config
from core.models import Reservation, Membre, Categorie, Cotisation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'membre']
        read_only_fields = ['id', 'username', 'email', 'membre']
        depth = 1


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

    def validate(self, data):
        config = read_config()
        if data.get("players") and data["players"][0] == data["players"][1]:
            raise serializers.ValidationError("les joueurs devraient être différent")
        number1 = Reservation.objects.filter(start_date__hour__range=[config['rule1']['From'], config['rule1']['To']],
                                            players__age__gte=config['rule1']['age']).count()

        number2 = Reservation.objects.filter(start_date__hour__range=[config['rule2']['From'], config['rule1']['To']]).count()

        number3 = Reservation.objects.filter(start_date__hour__range=[config['rule3']['From'], config['rule1']['To']],
                                            players__age__lte=config['rule3']['ageYoung']).count()

        if data.get('start_date').hour >= config['rule4']['hour']-1:
            data['eclairage_paye'] = True

        if number1 > config['rule1']['nb']:
            raise serializers.ValidationError("le nombre des joueurs autorisées a été dépassé")
        if number2 > config['rule2']['nbTrainer']:
            raise serializers.ValidationError("le nombre des joueurs autorisées a été dépassé")
        if number3 > config['rule3']['nb']:
            raise serializers.ValidationError("le nombre des joueurs autorisées a été dépassé")

        return data

    class Meta:
        model = Reservation
        fields = '__all__'
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        depth = 0


class ReservationSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['start_date', 'terrain']
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
                                             required=False, allow_null=True)

    # cotisation = serializers.SlugRelatedField(queryset=Cotisation.objects.all(), slug_field='pk', required=False)

    class Meta:
        model = Membre
        fields = '__all__'
        depth = 0
        # fields = ('url', 'id', 'nom', 'sexe', 'tel', 'age', 'date_naissance', 'mail', 'date_naissance', 'entraineur',
        #           'licence_fideration', 'cotisation', 'categorie')


class MembreLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        depth = 0
        fields = ('id', 'nom',)


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
