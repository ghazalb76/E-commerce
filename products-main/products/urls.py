from rest_framework.routers import DefaultRouter
from products.views import ProductViewset

router = DefaultRouter()
router.register(r'products', ProductViewset)

urlpatterns = router.urls

