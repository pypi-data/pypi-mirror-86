from rest_framework import serializers

from budget import models


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Budget
        fields = '__all__'
