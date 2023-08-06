from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from budget import serializers, models, filters


class BudgetListCreateView(generics.ListCreateAPIView):
    lookup_field = 'id'
    serializer_class = serializers.BudgetSerializer
    queryset = models.Budget.objects.all()
    permission_classes = (IsAuthenticated, )
    filterset_class = filters.BudgetFilter


class BudgetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = serializers.BudgetSerializer
    queryset = models.Budget.objects.all()
    permission_classes = (IsAuthenticated, )

