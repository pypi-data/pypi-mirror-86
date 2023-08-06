from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from budget import serializers, models, filters


class TransactionListCreateView(generics.ListCreateAPIView):
    lookup_field = 'id'
    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()
    permission_classes = (IsAuthenticated, )
    filterset_class = filters.TransactionFilter


class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()
    permission_classes = (IsAuthenticated, )
