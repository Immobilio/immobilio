from django_filters import rest_framework as filters
from .models import Program, Immobilier


class ProgramFilter(filters.FilterSet):
  
    class Meta:
        model = Program
        fields = {}
        for field in model._meta.fields:
            fields[field.name] = ['exact', 'lt', 'gt', 'in', 'isnull']


class ImmobilierFilter(filters.FilterSet):
  
    class Meta:
        model = Program
        fields = {}
        for field in model._meta.fields:
            fields[field.name] = ['exact', 'lt', 'gt', 'in', 'isnull']