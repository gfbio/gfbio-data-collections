from gfbio_collections.users.api.views import users_list_view, users_detail_view

from gfbio_collections.collections.api.views import (
    root_view,
    collection_view,
    collection_detail_view,
    )

from django.urls import path

app_name = "collections"

urlpatterns = [
    path('', view=root_view),
    path('collections/', view=collection_view, name='collections-list'),
    path('collections/<int:pk>/', view=collection_detail_view, name='collections-detail'),
    path('users/', view=users_list_view, name='user-list'),
    path('users/<str:username>/', view=users_detail_view, name='user-detail'),

]

