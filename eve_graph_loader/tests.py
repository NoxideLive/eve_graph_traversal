from typing import List

from django.test import TestCase

from eve_api import EveClient
from eve_api.models.stargate.Destination import Destination
from eve_api.models.station.Station import Station
from eve_api.models.system.System import System
from eve_graph_loader.loader.Loader import GraphLoader
# Create your tests here.
from utils import JSONHelpers


class EveClientTest(TestCase):

    def test_systems_get(self):
        systems = EveClient.get_systems()
        self.assertTrue(isinstance(systems, List))

    def test_system_get(self):
        correct_system = System(
            name="Tanoo",
            security_class="B",
            security_status=0.8583240509033203,
            star_id=40000001,
            stargates=[
                50000056,
                50000057,
                50000058
            ],
            stations=[
                60012526,
                60014437
            ],
            system_id=30000001
        )
        system = EveClient.get_system(30000001)
        self.assertDictEqual(correct_system.__dict__, system.__dict__)

    def test_station_get(self):
        correct_station = Station(
            name="Tanoo V - Moon 1 - Ammatar Consulate Bureau",
            station_id=60012526,
            system_id=30000001,
            type_id=2502,
            services=[
                "bounty-missions",
                "courier-missions",
                "interbus",
                "reprocessing-plant",
                "market",
                "stock-exchange",
                "cloning",
                "repair-facilities",
                "fitting",
                "news",
                "insurance",
                "docking",
                "office-rental",
                "loyalty-point-store",
                "navy-offices",
                "security-offices"
            ],
        )
        station = EveClient.get_station(60012526)
        self.assertDictEqual(correct_station.__dict__, station.__dict__)

    def test_stargate_destination_get(self):
        correct_destination = Destination(
            stargate_id=50000342,
            system_id=30000003
        )
        destination = EveClient.get_star_gate_destination(50000056)
        self.assertDictEqual(correct_destination.__dict__, destination.__dict__)


# Assumes Empty Database for Testing
class GraphLoaderTest(TestCase):
    graph_loader = GraphLoader()
    graph_loader.clear()

    def test_build_system_v(self):
        system = EveClient.get_system(30000001)
        self.graph_loader.build_system_v(system)
        v_system = self.graph_loader.get_system_v(system.system_id)
        self.assertIsNotNone(v_system, "System Vertex Build Failed")

    def test_update_system_v(self):
        system = EveClient.get_system(30000005)
        self.graph_loader.build_system_v(system)
        v_system = self.graph_loader.get_system_v(system.system_id)
        self.assertIsNotNone(v_system, "System Vertex Build Failed")
        system.security_class = 0.0111
        self.graph_loader.update_system_v(v_system, system)
        self.assertEqual(self.graph_loader.get_system_prop(system.system_id, "security_class"), '0.0111')

    def test_build_system_e(self):
        system1 = EveClient.get_system(30000002)
        v_system = self.graph_loader.build_system_v(system1)
        dest_systems = []
        for stargate_id in system1.stargates:
            destination = EveClient.get_star_gate_destination(stargate_id)
            dest_system = EveClient.get_system(destination.system_id)
            self.graph_loader.build_system_v(dest_system)
            dest_systems.append(destination.system_id)

        self.graph_loader.build_system_e(system1)
        self.assertTrue(
            self.graph_loader.g.V(v_system).outE("gate_to").inV().has("system", "system_id", dest_systems[0]).hasNext())
        self.assertTrue(
            self.graph_loader.g.V(v_system).outE("gate_to").inV().has("system", "system_id", dest_systems[1]).hasNext())

    def test_build_system_e_if_exists(self):
        system1 = EveClient.get_system(30000002)
        self.graph_loader.build_system_e(system1)
        v_system = self.graph_loader.get_system_v(system1.system_id)
        dest_systems = []
        for stargate_id in system1.stargates:
            destination = EveClient.get_star_gate_destination(stargate_id)
            dest_systems.append(destination.system_id)

        self.assertTrue(
            self.graph_loader.g.V(v_system).outE("gate_to").inV().has("system", "system_id", dest_systems[0]).hasNext())
        self.assertTrue(
            self.graph_loader.g.V(v_system).outE("gate_to").inV().has("system", "system_id", dest_systems[1]).hasNext())

    def test_build_station_v(self):
        system1 = EveClient.get_system(30000007)
        v_system = self.graph_loader.build_system_v(system1)

        station0 = EveClient.get_station(system1.stations[0])
        self.graph_loader.build_station_v(v_system, station0)
        self.assertTrue(self.graph_loader.g.V(v_system).outE("station").inV().has("station", "station_id",
                                                                                  station0.station_id).hasNext())
        self.assertEqual(self.graph_loader.get_station_system_v(station0.station_id), v_system)

        station1 = EveClient.get_station(system1.stations[1])
        self.graph_loader.build_station_v(v_system, station1)
        self.assertTrue(self.graph_loader.g.V(v_system).outE("station").inV().has("station", "station_id",
                                                                                  station1.station_id).hasNext())
        self.assertEqual(self.graph_loader.get_station_system_v(station1.station_id), v_system)

        station2 = EveClient.get_station(system1.stations[2])
        self.graph_loader.build_station_v(v_system, station2)
        self.assertTrue(self.graph_loader.g.V(v_system).outE("station").inV().has("station", "station_id",
                                                                                  station2.station_id).hasNext())
        self.assertEqual(self.graph_loader.get_station_system_v(station2.station_id), v_system)

    def test_build_station_v_if_exists(self):
        system1 = EveClient.get_system(30000007)
        v_system = self.graph_loader.get_system_v(system1.system_id)

        station0 = EveClient.get_station(system1.stations[0])
        self.graph_loader.build_station_v(v_system, station0)
        self.assertTrue(self.graph_loader.g.V(v_system).outE("station").inV().has("station", "station_id",
                                                                                  station0.station_id).hasNext())
        self.assertEqual(self.graph_loader.get_station_system_v(station0.station_id), v_system)

        station1 = EveClient.get_station(system1.stations[1])
        self.graph_loader.build_station_v(v_system, station1)
        self.assertTrue(self.graph_loader.g.V(v_system).outE("station").inV().has("station", "station_id",
                                                                                  station1.station_id).hasNext())
        self.assertEqual(self.graph_loader.get_station_system_v(station1.station_id), v_system)

        station2 = EveClient.get_station(system1.stations[2])
        self.graph_loader.build_station_v(v_system, station2)
        self.assertTrue(self.graph_loader.g.V(v_system).outE("station").inV().has("station", "station_id",
                                                                                  station2.station_id).hasNext())
        self.assertEqual(self.graph_loader.get_station_system_v(station2.station_id), v_system)


class UtilsTest(TestCase):

    def test_parse(self):
        bts = bytes('[1, 2, 3, 4]', 'utf-8')
        parsed_bytes = [1, 2, 3, 4]
        self.assertEqual(JSONHelpers.parse(bts), parsed_bytes)
