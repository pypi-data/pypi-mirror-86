from django_filters import rest_framework as django_filters

from api import models


class LineItemFilter(django_filters.FilterSet):
    owner = django_filters.CharFilter(field_name='owner__username', lookup_expr='exact')

    class Meta:
        model = models.LineItem
        fields = {
            'amount': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'type': ['exact'],
            'budget': ['exact'],
            'category': ['exact'],
            'sharing': ['exact']
        }
