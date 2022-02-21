from django.conf import settings
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import has, outE


class Navigator:
    connection = DriverRemoteConnection(f'ws://{settings.JANUS_URL}:8182/gremlin', 'g')
    g = traversal().withRemote(connection).withComputer()

    def station_to_system(self, station_from, system_to):
        self.g.V().has("station", "station_id", station_from).inE("station").inV().repeat(outE("gate_to").inV()).until(
            has("system", "system_id", system_to)).toList()

    def system_to_system(self, system_from, system_to):
        return self.g.V().has("system", "system_id", system_from).repeat(outE("gate_to").inV()).until(
            has("system", "system_id", system_to)).toList()
