from gfbio_collections.users.api.views import users_list_view, users_detail_view, users_me_view

from gfbio_collections.users.api.views import UserViewSet

from gfbio_collections.collection.api.views import (
    root_view,
    collection_list_view,
    collection_detail_view,
    collection_search_view,

)

from django.urls import path
from .api import views

app_name = "collection"

urlpatterns = [
    path('', view=root_view, name='root'),
    path('search/', view=collection_search_view, name='collection-search'),
    path('collection/', view=collection_list_view, name='collection-list'),
    path('collection/<str:username>/', view=collection_list_view, name='collection-list'),
    path('collection/<int:pk>/', view=collection_detail_view, name='collection-detail'),
    path('users/', view=users_list_view, name="users-list"),
    path('users/<str:username>/', view=users_detail_view, name="users-detail"),
    path('users/me/', view=users_me_view, name='user-me'),
    path('collection_list/', views.CollectionListView.as_view(), name='collection'),

]

