from django.urls import path
from .views import ModuleView, MasterDataView, ModuleUsersView, ProfileAPIView, ResourceTypeAPIView, WorkTypeAPIView
urlpatterns = [
    path('module/', ModuleView.as_view(), name='module-list'),
    path('module/<int:module_id>/', ModuleView.as_view(), name='module-detail'),
    path('masterdata/', MasterDataView.as_view(), name='masterdata-list'),
    path('masterdata/<int:resource_id>/', MasterDataView.as_view(), name='masterdata-detail'),
    path('module/<int:module_id>/users/', ModuleUsersView.as_view(), name='module-users'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('resource-types/', ResourceTypeAPIView.as_view(), name='resource-types'),
    path('work-types/', WorkTypeAPIView.as_view(), name='work-types'),
]
