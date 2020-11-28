from rest_framework import serializers

from core.models import Tournament, Membre


class TournamentSerializer(serializers.ModelSerializer):
    players = serializers.SlugRelatedField(many=True, queryset=Membre.objects.all(), slug_field='nom', required=False,
                                           allow_null=True)

    class Meta:
        model = Tournament
        fields = '__all__'


class TournamentLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'created_date']
        depth = 0
