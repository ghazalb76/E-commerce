from rest_framework.routers import DefaultRouter
from account.views import AccountViewset

router = DefaultRouter()
router.register(r'accounts', AccountViewset)

urlpatterns = router.urls
