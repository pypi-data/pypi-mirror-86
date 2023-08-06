from django_filters import rest_framework as django_filters

from api import models


class TransactionFilter(django_filters.FilterSet):
    owner = django_filters.CharFilter(field_name='owner__username', lookup_expr='exact')

    class Meta:
        model = models.Transaction
        fields = {
            'amount': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'type': ['exact'],
            'line_item': ['exact'],
            'merchant': ['exact'],
            'comment': ['contains'],
            'date': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'last_modified': ['lt', 'lte', 'gt', 'gte']
        }
