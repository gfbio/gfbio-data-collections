from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from gfbio_collections.users.api.views import UserViewSet
from gfbio_collections.collection.api.views import CollectionViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("collection", CollectionViewSet)

app_name = "api"
urlpatterns = router.urls
