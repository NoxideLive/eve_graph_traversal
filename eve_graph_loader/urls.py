from rest_framework import routers

from eve_graph_loader.views.GraphView import GraphViewSet

router = routers.SimpleRouter()
router.register(r'graph', GraphViewSet, 'graph')
urlpatterns = router.urls
