from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from gfbio_collections.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register(r'users', UserViewSet, basename='api')
# # #fixme: how to "register the viewset with a router" and get the urlconf automatically?
# app_name = "api"
# urlpatterns = router.urls
