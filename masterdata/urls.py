from django.urls import path
from .views import CategoryView, MasterDataView
urlpatterns = [
    path('category/', CategoryView.as_view(), name='module-list'),
    path('category/<int:module_id>/', CategoryView.as_view(), name='module-detail'),
    path('masterdata/', MasterDataView.as_view(), name='masterdata-list'),
    path('masterdata/<int:resource_id>/', MasterDataView.as_view(), name='masterdata-detail'),
]