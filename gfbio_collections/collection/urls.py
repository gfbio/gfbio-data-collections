from gfbio_collections.users.api.views import users_list_view, users_detail_view, users_me_view

from gfbio_collections.users.api.views import UserViewSet

from gfbio_collections.collection.api.views import (
    root_view,
    collection_view,
    collection_detail_view,
    collection_search_view,

)

from django.urls import path

app_name = "collection"

urlpatterns = [
    path('', view=root_view),
    path('collections/', view=collection_view, name='collections-list'),
    path('search/', view=collection_search_view, name='collections-search'),
    path('collections/<int:pk>/', view=collection_detail_view, name='collections-detail'),
    path('collections/<str:username>/', view=collection_view, name='collections-list'),
    path('users/', view=users_list_view, name="users-list"),
    path('users/<str:username>/', view=users_detail_view, name="users-detail"),
    path('users/me/', view=users_me_view, name='user-me')
]

