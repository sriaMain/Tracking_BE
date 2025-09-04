# from django.urls import path
# from .views import EstimationCreateAPIView, PaymentTrackingAPIView, ProjectPaymentMilestoneAPIView, ProjectEstimationAPIView, ProjectPaymentTrackingAPIView, ProjectEstimationPaymentAPIView

# urlpatterns = [
  
  
#     path('estimation/create/', EstimationCreateAPIView.as_view(), name='estimation-create'),
#     path('estimation/<int:pk>/', EstimationCreateAPIView.as_view(), name='estimation-detail'),
#     path('payment-tracking/', PaymentTrackingAPIView.as_view()),
#     path('payment-tracking/<int:pk>/', PaymentTrackingAPIView.as_view()),

#     path('payment-milestone/', ProjectPaymentMilestoneAPIView.as_view()),
#     path('payment-milestone/<int:pk>/', ProjectPaymentMilestoneAPIView.as_view()),
#     # path("projects/<int:project_id>/profit-loss-advanced/", ProfitLossAdvancedAPIView.as_view(), name="profit-loss-advanced"),
#     path('project/<int:project_id>/estimation/', ProjectEstimationAPIView.as_view(), name='project-estimation'),
#     path('project/<int:project_id>/payments/', ProjectPaymentTrackingAPIView.as_view(), name='project-payments'),
#     path('project/<int:project_id>/estimation/payment/', ProjectEstimationPaymentAPIView.as_view(), name='project-financial-detail'),
 

 
# ]


from django.urls import path
from .views import (
    PaymentListCreateAPIView, PaymentDetailAPIView,
    MilestoneListCreateAPIView, MilestoneDetailAPIView,
    TransactionCreateAPIView, AdditionalRequestListCreateAPIView,
    AdditionalRequestApproveAPIView, NotificationListAPIView,
    RuleListCreateAPIView
)

urlpatterns = [
    path("payments/", PaymentListCreateAPIView.as_view(), name="payments-list"),
    path("payments/<int:pk>/", PaymentDetailAPIView.as_view(), name="payments-detail"),

    path("milestones/", MilestoneListCreateAPIView.as_view(), name="milestones-list"),
    path("milestones/<int:pk>/", MilestoneDetailAPIView.as_view(), name="milestones-detail"),

    path("transactions/", TransactionCreateAPIView.as_view(), name="transactions-create"),

    path("additional-requests/", AdditionalRequestListCreateAPIView.as_view(), name="additional-list"),
    path("additional-requests/<int:req_id>/approve/", AdditionalRequestApproveAPIView.as_view(), name="additional-approve"),
    path("additional-requests/<int:req_id>/reject/", AdditionalRequestApproveAPIView.as_view(), name="additional-reject"),

    path("notifications/", NotificationListAPIView.as_view(), name="notifications"),
    path("rules/", RuleListCreateAPIView.as_view(), name="rules")
]
