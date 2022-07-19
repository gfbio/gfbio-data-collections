from django.urls import path
from .api import views


app_name = "collection"

urlpatterns = [
    path('', views.CollectionListView.as_view(), name='collections-create'),
    path('<uuid:pk>/', views.CollectionDetailView.as_view(), name='collections-detail'),
    path('users/<external_user_id>/', views.UserCollectionListView.as_view(), name='collections-for-user'),
]
