#!/usr/bin/env python3.9
from rest_framework import serializers
from bestservo.models import ServiceStations

class ServiceStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceStations
        fields = ['id', 'description', 'brand', 'date', 'price', 'trading_name', 'location', 'address', 'phone', 'latitude', 'longitude', 'site_features']
