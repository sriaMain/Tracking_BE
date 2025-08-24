from django.urls import path
from .views import DocumentUploadAPIView,DocumentListAPIView,EstimationCreateAPIView  

urlpatterns = [
  
  
    path('estimation/create/', EstimationCreateAPIView.as_view(), name='estimation-create'),
    path('upload/', DocumentUploadAPIView.as_view(), name='document-upload'),
    path('documents/<int:pk>/delete/', DocumentListAPIView.as_view(), name='document-delete'),
    
 

 
]