from django.urls import path
from .api.views import CollectionAPIView


app_name = "collection"

collections_detail = CollectionAPIView.as_view({
    'get': 'retrieve'
})

collections_for_user = CollectionAPIView.as_view({
    'get': 'get_collections_for_user'
})

urlpatterns = [
    path('<uuid:pk>/', collections_detail, name='collections-detail'),
    path('users/<external_user_id>/', collections_for_user, name='collections-for-user'),
]
