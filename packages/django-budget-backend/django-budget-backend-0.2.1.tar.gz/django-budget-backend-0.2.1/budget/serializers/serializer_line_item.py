from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from budget import common_text as text
from budget import models


class LineItemSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True)

    class Meta:
        model = models.LineItem
        fields = '__all__'

    def create(self, validated_data):
        if validated_data['sharing'] == 'personal':
            request = self.context.get('request')
            validated_data['owner'] = request.user
        return super().create(validated_data)

    def validate_sharing(self, value):
        if self.instance is not None and self.instance.sharing != value:
            raise ValidationError(text.template_cannot_edit_property.format('sharing'))
        return value
