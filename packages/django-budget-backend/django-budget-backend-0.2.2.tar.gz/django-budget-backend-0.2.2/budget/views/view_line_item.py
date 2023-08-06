from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from budget import serializers, models, filters


class LineItemListCreateView(generics.ListCreateAPIView):
    lookup_field = 'id'
    serializer_class = serializers.LineItemSerializer
    queryset = models.LineItem.objects.all()
    permission_classes = (IsAuthenticated, )
    filterset_class = filters.LineItemFilter


class LineItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = serializers.LineItemSerializer
    queryset = models.LineItem.objects.all()
    permission_classes = (IsAuthenticated, )
