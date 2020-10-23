from rest_framework import serializers

from school.models import School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class SchoolLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name']
        depth = 0
