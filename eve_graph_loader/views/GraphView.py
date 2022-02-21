from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from eve_api import EveClient
from eve_graph_loader.loader.Loader import GraphLoader


class GraphViewSet(ViewSet):

    def list(self, request, format=None):
        graph_loader = GraphLoader()
        return Response()

    @action(detail=False, methods=['GET'])
    def load_v(self, request):
        graph_loader = GraphLoader()
        graph_loader.load_v()
        return Response(status=200)

    @action(detail=False, methods=['GET'])
    def count(self, request):
        graph_loader = GraphLoader()
        return Response(graph_loader.v_count())

    @action(detail=False, methods=['GET'])
    def load_e(self, request):
        graph_loader = GraphLoader()
        graph_loader.load_e()
        return Response(status=200)

    @action(detail=False, methods=['GET'])
    def test(self, request):
        systems = EveClient.get_systems()
        system = EveClient.get_system(systems[0])
        graph_loader = GraphLoader()

        return Response(graph_loader.v_count())
