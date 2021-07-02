from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from nfdi_collection.users.api.views import UserViewSet
from nfdi_collection.dataid.api.views import DataIdViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("dataid", DataIdViewSet)


app_name = "api"
urlpatterns = router.urls
