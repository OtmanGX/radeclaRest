from rest_framework.filters import BaseFilterBackend


def convert(value):
    print("str")
    if value.isdigit():
        return float(value)
    return value


class FilterSearch(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_fields = self.get_filter_fields(view, request)
        if filter_fields is None or len(filter_fields) == 0:
            filter_fields = [field.name for field in queryset.model()._meta.fields]
            filter_fields = [field for field in request.query_params.keys()
                             if field.split("_")[0] in filter_fields]
        filter_fields = {
            field: convert(request.query_params.get(field))
            for field in filter_fields if request.query_params.get(field, False)}
        queryset = queryset.filter(**filter_fields)
        return queryset

    def get_filter_fields(self, view, request):
        return getattr(view, 'filter_fields', None)

    def get_schema_fields(self, view):
        return super().get_schema_fields(view)

    def get_schema_operation_parameters(self, view):
        return super().get_schema_operation_parameters(view)
