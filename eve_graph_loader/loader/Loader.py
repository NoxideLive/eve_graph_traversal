import math
from threading import Thread
from typing import List

from django.conf import settings
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal

from eve_api import EveClient


def chunks(lst, n):
    count = math.floor(len(lst) / n)
    for i in range(0, len(lst), count):
        yield lst[i:i + count]


class GraphLoader:
    connection = DriverRemoteConnection(f'ws://{settings.JANUS_URL}:8182/gremlin', 'g')
    load_threads = []
    thread_count = 25
    g = traversal().withRemote(connection)

    def __init__(self):
        pass

    def get_system_v(self, v_id):
        return self.g.V().has("system", "system_id", v_id).next()

    def get_system_prop(self, v_id, key):
        return self.g.V().has("system", "system_id", v_id).values(key).next()

    def get_station_v(self, v_id):
        return self.g.V().has("station", "station_id", v_id).next()

    def get_station_system_v(self, v_id):
        return self.g.V().has("station", "station_id", v_id).in_("station").next()

    def v_count(self):
        return self.g.V().count().next()

    def clear(self):
        return self.g.V().drop().iterate()

    def load_v(self):
        system_ids = EveClient.get_systems()
        print(f'Adding {len(system_ids)} systems to graph')

        self.g.V().hasLabel("system").index().iterate()

        def load_func(systems_ids: List[int]):
            for system_id in systems_ids:
                system = EveClient.get_system(system_id)
                print(f'Got System {system_id}')
                v_system = self.g.V().has("system", "system_id", system_id)
                if v_system.hasNext():
                    v_system = v_system.next()
                    self.update_system_v(v_system, system)
                else:
                    v_system = self.build_system_v(system)
                for station_id in system.stations:
                    station = EveClient.get_station(station_id)
                    self.build_station_v(v_system, station)

        ids = list(chunks(system_ids, self.thread_count))
        for x in range(self.thread_count):
            thread = Thread(target=load_func, args=(ids[x],))
            thread.start()
            self.load_threads.append(thread)

    def load_e(self):
        system_ids = EveClient.get_systems()

        def load_func(systems_ids: List[int]):
            for system_id in systems_ids:
                system = EveClient.get_system(system_id)
                self.build_system_e(system)

        ids = list(chunks(system_ids, self.thread_count))
        for x in range(self.thread_count):
            thread = Thread(target=load_func, args=(ids[x],))
            thread.start()
            self.load_threads.append(thread)

    def build_system_v(self, system):
        v = self.g.addV('system')
        for prop in system.vertex_properties:
            v.property(prop, system.__getattribute__(prop))
        return v.next()

    def update_system_v(self, system_v, system):
        sys = self.g.V(system_v)
        for prop in system.vertex_properties:
            sys.property(prop, system.__getattribute__(prop))
        return sys.next()

    def build_system_e(self, system):
        v = self.g.V().has("system", "system_id", system.system_id)
        if v.hasNext():
            v = v.next()
            print(f'Found V {v} for {system.system_id}')
            for stargate_id in system.stargates:
                destination = EveClient.get_star_gate_destination(stargate_id)
                edge = self.g.V(v).outE("gate_to").inV().has("system", "system_id", destination.system_id)
                if not edge.hasNext():
                    v_lookup = self.g.V().has("system", "system_id", destination.system_id)
                    if v_lookup.hasNext():
                        v_dest = v_lookup.next()
                        print(f'Found V {v_dest} destination for Star Gate {stargate_id}')
                        print(f'Adding Gate Edge from {v} to {v_dest}')
                        self.g.V(v).addE("gate_to").to(v_dest).iterate()
                    else:
                        print(f'No Destination Node found for Star Gate {stargate_id}')
                        # TODO Possibly Create Vertex here. Thread Safety??
                else:
                    print(f"Has edge from {system.system_id} to {destination.system_id}")
        else:
            print(f"No Vertex Found for {system.system_id}")

    def build_station_v(self, v_system, station):
        v_station = self.g.V().has("station", "station_id", station.station_id)
        if not v_station.hasNext():
            v_station = self.g.V(v_system).as_("origin").addV("station")
            for prop in station.vertex_properties:
                v_station.property(prop, station.__getattribute__(prop))
            v_station.as_("dest").addE("station").from_("origin").to("dest").next()
        else:
            v_station = v_station.next()
            v_dest_edge = self.g.V(v_system).outE('station').inV().has("station", "station_id", station.station_id)
            if not v_dest_edge.hasNext():
                self.g.V(v_system).addE("station").to(v_station).next()
            else:
                print(f"Has edge from {v_system} to {v_station}")
