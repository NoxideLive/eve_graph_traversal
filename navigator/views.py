# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from navigator.navigate.Navigator import Navigator


class NavigatorViewSet(viewsets.ViewSet):
    parser_classes = [JSONParser]

    @action(detail=False, methods=['POST'])
    def system_to_system(self, request):
        navigator = Navigator()
        print(navigator.system_to_system(request.data['systemFrom'], request.data['systemTo']))
        return Response(status=200)
