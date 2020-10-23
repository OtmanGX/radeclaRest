from rest_framework import viewsets
from rest_framework.response import Response
from radeclaRest.utils import StandardResultsSetPagination
from school.models import School
from school.serializers import SchoolSerializer, SchoolLiteSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        is_all = request.GET.get('all', None)
        if is_all:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = SchoolLiteSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return super().list(self, request, *args, **kwargs)
