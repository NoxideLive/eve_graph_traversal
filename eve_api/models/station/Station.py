from typing import List

from rest_framework import serializers


class Station:
    station_id: int
    system_id: int
    type_id: int
    name: str
    services: List[str]

    vertex_properties = ["station_id", "system_id", "type_id", "name"]

    def __init__(self, name, station_id, system_id, type_id, services=None):
        self.name = name
        self.station_id = station_id
        self.system_id = system_id
        self.type_id = type_id
        self.services = services


class StationSerializer(serializers.Serializer):
    station_id = serializers.IntegerField()
    system_id = serializers.IntegerField()
    type_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    services = serializers.ListSerializer(
        child=serializers.CharField(max_length=100)
    )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return Station(**validated_data)
