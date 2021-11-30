from gfbio_collection.users.api.views import users_list_view, users_detail_view

from gfbio_collection.collection.api.views import (
    root_view,
    collection_view,
    collection_detail_view,
    )

from django.urls import path

app_name = "collection"

urlpatterns = [
    path('', view=root_view),
    path('collection/', view=collection_view, name='collection-list'),
    path('collection/<int:pk>/', view=collection_detail_view, name='collection-detail'),
    path('users/', view=users_list_view, name='user-list'),
    path('users/<str:username>/', view=users_detail_view, name='user-detail'),

]

