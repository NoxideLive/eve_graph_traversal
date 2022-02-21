from typing import List

from rest_framework import serializers


class System:
    name: str
    security_class: str
    security_status: float
    star_id: int
    stargates: List[int]
    system_id: int

    vertex_properties = ["name", "security_class", "security_status", "star_id", "system_id"]

    def __init__(self, name: str,
                 system_id: int,
                 star_id: int = None,
                 security_class: str = None,
                 security_status: float = None,
                 stargates=None,
                 stations=None):
        if stargates is None:
            stargates = list()
        if stations is None:
            stations = list()
        self.name = name
        self.security_class = security_class
        self.security_status = security_status
        self.star_id = star_id
        self.system_id = system_id
        self.stargates = stargates
        self.stations = stations


class SystemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    security_class = serializers.CharField(max_length=100, required=False)
    security_status = serializers.FloatField(required=False)
    system_id = serializers.IntegerField()
    star_id = serializers.IntegerField(required=False)

    stargates = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False
    )

    stations = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False
    )

    def create(self, validated_data):
        return System(**validated_data)

    def update(self, instance: System, validated_data):
        pass
