from django.urls import path
from .views import ClientListCreateAPIView, ClientDetailAPIView,ProjectListCreateAPIView,ProjectDetailAPIView,ClientPocCreateAPIView, ClientPocDetailAPIView  

urlpatterns = [
  
    path('clients/', ClientListCreateAPIView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientDetailAPIView.as_view(), name='client-detail'),
    path('clients/poc/', ClientPocCreateAPIView.as_view(), name='client-poc-list-create'),
    path('clients/poc/<int:pk>/', ClientPocDetailAPIView.as_view(), name='client-poc-detail'),
    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    # path('id/', IdView.as_view(), name='project-list-create'),
 

 
]