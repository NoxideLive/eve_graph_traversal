from typing import List

import requests
from django.conf import settings

from eve_api.models.stargate import Destination
from eve_api.models.stargate.Destination import DestinationSerializer
from eve_api.models.station import Station
from eve_api.models.station.Station import StationSerializer
from eve_api.models.system import System
from eve_api.models.system.System import SystemSerializer

API_URL = settings.EVE_API_URL


class EveClient:

    @staticmethod
    def get_systems() -> List[int]:
        r = requests.get(f'{API_URL}/universe/systems/')
        return r.json()

    @staticmethod
    def get_system(system_id: int) -> System:
        r = requests.get(f'{API_URL}/universe/systems/{system_id}')
        serializer = SystemSerializer(data=r.json())
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def get_station(station_id: int) -> Station:
        r = requests.get(f'{API_URL}/universe/stations/{station_id}')
        serializer = StationSerializer(data=r.json())
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def get_star_gate_destination(gate_id) -> Destination:
        r = requests.get(f'{API_URL}/universe/stargates/{gate_id}')
        serializer = DestinationSerializer(data=r.json()['destination'])
        serializer.is_valid(raise_exception=True)
        return serializer.save()
