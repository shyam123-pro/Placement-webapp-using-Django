from rest_framework import serializers
from .models import NOCRequest

class NOCRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = NOCRequest
        fields = '__all__'
