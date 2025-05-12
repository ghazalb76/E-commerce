from orders.views import OrderViewSet, CartViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders/(?P<username>\w+)', OrderViewSet, basename='orders')
router.register(r'carts/(?P<username>\w+)', CartViewSet, basename='carts')

urlpatterns = router.urls
