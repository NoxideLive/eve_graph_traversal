from rest_framework import serializers


class Destination:
    stargate_id: int
    system_id: int

    def __init__(self, stargate_id, system_id):
        self.stargate_id = stargate_id
        self.system_id = system_id


class DestinationSerializer(serializers.Serializer):
    stargate_id = serializers.IntegerField()
    system_id = serializers.IntegerField()

    def create(self, validated_data):
        return Destination(**validated_data)

    def update(self, instance, validated_data):
        pass
