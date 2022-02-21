from rest_framework import serializers

from eve_api.models.stargate import Destination
from eve_api.models.stargate.Destination import DestinationSerializer


class StarGate:
    destination: Destination
    name: str

    def __init__(self, destination: Destination, name: str):
        self.destination = destination
        self.name = name


class StarGateSerializer(serializers.Serializer):
    destination = DestinationSerializer()
    name = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return StarGate(**validated_data)
