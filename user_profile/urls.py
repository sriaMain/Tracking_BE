from django.urls import path
from .views import ModuleView, MasterDataView
urlpatterns = [
    path('module/', ModuleView.as_view(), name='module-list'),
    path('module/<int:module_id>/', ModuleView.as_view(), name='module-detail'),
    path('masterdata/', MasterDataView.as_view(), name='masterdata-list'),
    path('masterdata/<int:resource_id>/', MasterDataView.as_view(), name='masterdata-detail'),
]