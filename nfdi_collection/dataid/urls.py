from nfdi_collection.users.api.views import users_list_view, users_detail_view

from nfdi_collection.dataid.api.views import (
    root_view,
    dataid_view,
    dataid_detail_view,
    )

from django.urls import path

app_name = "dataid"

urlpatterns = [
    path('', view=root_view),
    path('dataid/', view=dataid_view, name='dataid-list'),
    path('dataid/<int:pk>/', view=dataid_detail_view, name='dataid-detail'),
    path('users/', view=users_list_view, name='user-list'),
    path('users/<str:username>/', view=users_detail_view, name='user-detail'),

]

