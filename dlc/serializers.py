from rest_framework import serializers
from dlc.models import DLC


class DLCSerializer(serializers.ModelSerializer):
    class Meta:
         model = DLC
         fields = ('id', 'dlc','links')