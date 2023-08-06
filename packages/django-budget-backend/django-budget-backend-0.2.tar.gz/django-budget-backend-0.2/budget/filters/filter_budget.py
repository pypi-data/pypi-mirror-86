from django_filters import rest_framework as django_filters

from budget import models


class BudgetFilter(django_filters.FilterSet):
    class Meta:
        model = models.Budget
        fields = {
            'start_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'end_date': ['exact', 'lt', 'lte', 'gt', 'gte']
        }
