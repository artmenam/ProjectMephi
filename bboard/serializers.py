from rest_framework import serializers
from .models import pred
class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = pred
        fields = ('Date', 'Price')