from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api import common_text as text
from api import models


class TransactionSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True)

    class Meta:
        model = models.Transaction
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)

    def validate(self, attrs):
        # validate the date with budget start and end date
        date = attrs.get('date')
        budget = attrs.get('line_item').budget
        if date < budget.start_date or date > budget.end_date:
            raise ValidationError(text.template_date_out_of_range.format(date, budget.start_date, budget.end_date))
        return attrs
