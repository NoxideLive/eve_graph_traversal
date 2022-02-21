from rest_framework import routers

from navigator.views import NavigatorViewSet

router = routers.SimpleRouter()
router.register(r'navigate', NavigatorViewSet, 'navigate')
urlpatterns = router.urls
