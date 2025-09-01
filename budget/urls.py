from django.urls import path
from .views import EstimationCreateAPIView, ProjectPaymentTrackingAPIView, ProjectPaymentMilestoneAPIView 

urlpatterns = [
  
  
    path('estimation/create/', EstimationCreateAPIView.as_view(), name='estimation-create'),
    path('payment-tracking/', ProjectPaymentTrackingAPIView.as_view()),
    path('payment-tracking/<int:pk>/', ProjectPaymentTrackingAPIView.as_view()),

    path('payment-milestone/', ProjectPaymentMilestoneAPIView.as_view()),
    path('payment-milestone/<int:pk>/', ProjectPaymentMilestoneAPIView.as_view()),
   
 

 
]