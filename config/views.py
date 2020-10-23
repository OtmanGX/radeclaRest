from django.shortcuts import render
from rest_framework.status import HTTP_400_BAD_REQUEST
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.apps import read_config
from config.serializers import RuleOneSerializer, RuleFourSerializer, RuleThreeSerializer, RuleTwoSerializer


@api_view(['GET', 'POST'])
def read_config_request(request):
    if request.method == 'POST':
        print(request.data)
        if request.data.get('hour', None):
            serializer = RuleFourSerializer(data=request.data)
        elif request.data.get('ageYoung', None):
            serializer = RuleThreeSerializer(data=request.data)
        elif request.data.get('nbTrainer', None):
            serializer = RuleTwoSerializer(data=request.data)
        else:
            serializer = RuleOneSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    config = read_config()
    return Response(config)
