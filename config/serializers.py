from rest_framework import serializers

from config.apps import write_config


class RuleOneSerializer(serializers.Serializer):
    From = serializers.IntegerField(min_value=8)
    To = serializers.IntegerField(max_value=24)
    age = serializers.IntegerField(max_value=100)
    nb = serializers.IntegerField(max_value=9)

    def save(self, **kwargs):
        config = write_config(rule1=self.validated_data)
        return config


class RuleTwoSerializer(serializers.Serializer):
    From = serializers.IntegerField(min_value=8)
    To = serializers.IntegerField(max_value=24)
    nbTrainer = serializers.IntegerField(max_value=9)

    def save(self, **kwargs):
        config = write_config(rule2=self.validated_data)
        return config


class RuleThreeSerializer(serializers.Serializer):
    From = serializers.IntegerField(min_value=8)
    To = serializers.IntegerField(max_value=24)
    ageYoung = serializers.IntegerField(max_value=100)
    nb = serializers.IntegerField(max_value=9)

    def save(self, **kwargs):
        config = write_config(rule3=self.validated_data)
        return config


class RuleFourSerializer(serializers.Serializer):
    hour = serializers.IntegerField(min_value=8)

    def save(self, **kwargs):
        config = write_config(rule4=self.validated_data)
        return config
