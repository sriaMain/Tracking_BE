from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ProjectEstimation, ProjectPaymentTracking, ProjectPaymentMilestone
from .serializers import EstimationSerializer, ProjectPaymentTrackingSerializer, ProjectPaymentMilestoneSerializer
from django.core.exceptions import ValidationError  


# Create your views here.
    
class EstimationCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = EstimationSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save(created_by=request.user)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        estimations = ProjectEstimation.objects.all()
        serializer = EstimationSerializer(estimations, many=True)
        return Response(serializer.data)    
    def put(self, request, pk):
        estimation = get_object_or_404(ProjectEstimation, pk=pk)
        serializer = EstimationSerializer(estimation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def handle_exception(self, exc):
    #     """
    #     Centralized exception handling for consistent error responses.
    #     """
    #     if isinstance(exc, ValidationError):
    #         return Response(
    #             {"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST
    #         )
    #     return Response(
    #         {"error": "Internal server error", "details": str(exc)},
    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     )

    # def post(self, request):
    #     """Create a new Project Estimation"""
    #     try:
    #         serializer = EstimationSerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         estimation = EstimationService.create_estimation(
    #             serializer.validated_data, request.user
    #         )
    #         return Response(
    #             EstimationSerializer(estimation).data,
    #             status=status.HTTP_201_CREATED,
    #         )
    #     except Exception as exc:
    #         return self.handle_exception(exc)

    # def get(self, request, pk=None):
    #     """Retrieve single estimation or list all"""
    #     try:
    #         if pk:
    #             estimation = EstimationService.get_estimation(pk)
    #             return Response(EstimationSerializer(estimation).data)

    #         estimations = EstimationService.list_estimations()
    #         return Response(EstimationSerializer(estimations, many=True).data)

    #     except Exception as exc:
    #         return self.handle_exception(exc)

    # def put(self, request, pk):
    #     """Update an estimation"""
    #     try:
    #         serializer = EstimationSerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         estimation = EstimationService.update_estimation(
    #             pk, serializer.validated_data, request.user
    #         )
    #         return Response(EstimationSerializer(estimation).data)
    #     except Exception as exc:
    #         return self.handle_exception(exc)

    # def delete(self, request, pk):
    #     """Delete an estimation"""
    #     try:
    #         EstimationService.delete_estimation(pk)
    #         return Response(
    #             {"message": f"Estimation {pk} deleted successfully"},
    #             status=status.HTTP_204_NO_CONTENT,
    #         )
    #     except Exception as exc:
    #         return self.handle_exception(exc)




# class PaymentTrackingAPIView(APIView):         2222222222222
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def get(self, request, pk=None):
#         if pk:
#             tracking = get_object_or_404(ProjectPaymentTracking, pk=pk)
#             serializer = ProjectPaymentTrackingSerializer(tracking)
#             return Response(serializer.data)
#         else:
#             tracking = ProjectPaymentTracking.objects.all()
#             serializer = ProjectPaymentTrackingSerializer(tracking, many=True)
#             return Response(serializer.data)

#     def post(self, request):
#         serializer = ProjectPaymentTrackingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         tracking = get_object_or_404(ProjectPaymentTracking, pk=pk)
#         serializer = ProjectPaymentTrackingSerializer(tracking, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         tracking = get_object_or_404(ProjectPaymentTracking, pk=pk)
#         tracking.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# class ProjectPaymentMilestoneAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def get(self, request, pk=None):
#         if pk:
#             milestone = get_object_or_404(ProjectPaymentMilestone, pk=pk)
#             serializer = ProjectPaymentMilestoneSerializer(milestone)
#             return Response(serializer.data)
#         else:
#             milestones = ProjectPaymentMilestone.objects.all()
#             serializer = ProjectPaymentMilestoneSerializer(milestones, many=True)
#             return Response(serializer.data)

#     def post(self, request):
#         serializer = ProjectPaymentMilestoneSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         milestone = get_object_or_404(ProjectPaymentMilestone, pk=pk)
#         serializer = ProjectPaymentMilestoneSerializer(milestone, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         milestone = get_object_or_404(ProjectPaymentMilestone, pk=pk)
#         milestone.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)  2222222222222222222


# class ProjectPaymentMilestoneAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def post(self, request):
#         serializer = ProjectPaymentMilestoneSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(data=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    

# class ProfitLossAdvancedAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def get(self, request, project_id):
#         data = calculate_project_profit_loss(project_id)
#         serializer = ProfitLossSerializer(data)
#         return Response(serializer.data)



class ProjectEstimationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
    Fetch latest estimation for a given project.
    """
    def get(self, request, project_id, format=None):
        estimation = ProjectEstimation.objects.filter(project_id=project_id).last()
        if not estimation:
            return Response({"error": "No estimation found for this project."}, status=status.HTTP_404_NOT_FOUND)

        estimation_data = {
            "id": estimation.id,
            "estimation_date": estimation.estimation_date,
            # Use str() to return human-readable value from UserRole's __str__ method
            "estimation_provider": str(estimation.estimation_provider) if estimation.estimation_provider else None,
            "estimation_review": str(estimation.estimation_review) if estimation.estimation_review else None,
            "initial_estimation_amount": estimation.initial_estimation_amount,
            "approved_estimation": estimation.approved_estimation,
            "purchase_order_status": estimation.purchase_order_status,
            "created_at": estimation.created_at,
            "modified_at": estimation.modified_at,
            "created_by": estimation.created_by.id if estimation.created_by else None,
            "modified_by": estimation.modified_by.id if estimation.modified_by else None,
        }

        return Response(estimation_data, status=status.HTTP_200_OK)


class ProjectPaymentTrackingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
    Fetch all payment tracking and milestones for a given project.
    """
    def get(self, request, project_id, format=None):
        payments = ProjectPaymentTracking.objects.filter(project_id=project_id)
        if not payments.exists():
            return Response({"error": "No payments found for this project."}, status=status.HTTP_404_NOT_FOUND)

        payment_list = []
        for payment in payments:
            milestones = payment.milestones.all()
            milestone_list = [
                {
                    "id": m.id,
                    "name": m.name,
                    "amount": m.amount,
                    "due_date": m.due_date
                } for m in milestones
            ]

            payment_list.append({
                "id": payment.id,
                "payment_type": payment.payment_type,
                "other_payment_type": payment.other_payment_type,
                "approved_budget": payment.approved_budget,
                "additional_amount": payment.additional_amount,
                "payout": payment.payout,
                "pending": payment.pending,
                "hold": payment.hold,
                "hold_reason": payment.hold_reason,
                "created_at": payment.created_at,
                "modified_at": payment.modified_at,
                "created_by": payment.created_by.id if payment.created_by else None,
                "modified_by": payment.modified_by.id if payment.modified_by else None,
                "milestones": milestone_list,
            })

        return Response(payment_list, status=status.HTTP_200_OK)


class ProjectEstimationPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
    Fetch both estimation and payment tracking (with milestones) for a given project.
    """
    def get(self, request, project_id, format=None):
        # --- Fetch latest estimation ---
        estimation = ProjectEstimation.objects.filter(project_id=project_id).last()
        if estimation:
            estimation_data = {
                "id": estimation.id,
                "estimation_date": estimation.estimation_date,
                "estimation_provider": str(estimation.estimation_provider) if estimation.estimation_provider else None,
                "estimation_review": str(estimation.estimation_review) if estimation.estimation_review else None,
                "initial_estimation_amount": estimation.initial_estimation_amount,
                "approved_estimation": estimation.approved_estimation,
                "purchase_order_status": estimation.purchase_order_status,
                "created_at": estimation.created_at,
                "modified_at": estimation.modified_at,
                "created_by": estimation.created_by.id if estimation.created_by else None,
                "modified_by": estimation.modified_by.id if estimation.modified_by else None,
            }
        else:
            estimation_data = None

        # --- Fetch all payment tracking ---
        payments = ProjectPaymentTracking.objects.filter(project_id=project_id)
        payment_list = []
        for payment in payments:
            milestones = payment.milestones.all()
            milestone_list = [
                {
                    "id": m.id,
                    "name": m.name,
                    "amount": m.amount,
                    "due_date": m.due_date
                } for m in milestones
            ]

            payment_list.append({
                "id": payment.id,
                "payment_type": payment.payment_type,
                "other_payment_type": payment.other_payment_type,
                "approved_budget": payment.approved_budget,
                "additional_amount": payment.additional_amount,
                "payout": payment.payout,
                "pending": payment.pending,
                "hold": payment.hold,
                "hold_reason": payment.hold_reason,
                "created_at": payment.created_at,
                "modified_at": payment.modified_at,
                "created_by": payment.created_by.id if payment.created_by else None,
                "modified_by": payment.modified_by.id if payment.modified_by else None,
                "milestones": milestone_list,
            })

        return Response({
            "estimation": estimation_data,
            "payments": payment_list
        }, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ProjectPaymentTrackingSerializer, ProjectPaymentMilestoneSerializer,
    PaymentTransactionSerializer, AdditionalBudgetRequestSerializer, NotificationSerializer, RuleSerializer
)
from .models import ProjectPaymentTracking, ProjectPaymentMilestone, PaymentTransaction, AdditionalBudgetRequest, Notification, Rule
from .services import create_payment, update_payment, get_payment
from .services import create_milestone
from .services import create_transaction
from .services import request_additional, approve_request, reject_request
from .services import evaluate_and_notify
from .permission import IsFinanceApprover
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .services import notify_budget_request,  notify_milestone_update, notify_budget_breach

# Payment endpoints
class PaymentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        qs = ProjectPaymentTracking.objects.all()
        ser = ProjectPaymentTrackingSerializer(qs, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = ProjectPaymentTrackingSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        p = create_payment(ser.validated_data, request.user)
        return Response(ProjectPaymentTrackingSerializer(p).data, status=status.HTTP_201_CREATED)


class PaymentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]    

    def get_object(self, pk):
        return get_payment(pk)

    def get(self, request, pk):
        p = self.get_object(pk)
        return Response(ProjectPaymentTrackingSerializer(p).data)

    def patch(self, request, pk):
        ser = ProjectPaymentTrackingSerializer(instance=self.get_object(pk), data=request.data, partial=True, context={"request": request})
        ser.is_valid(raise_exception=True)
        p = update_payment(pk, ser.validated_data, request.user)
        return Response(ProjectPaymentTrackingSerializer(p).data)

    def delete(self, request, pk):
        obj = get_payment(pk)
        obj.delete()
        return Response({"detail": "Deleted"}, status=status.HTTP_204_NO_CONTENT)


# Milestones
class MilestoneListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]    

    def get(self, request):
        qs = ProjectPaymentMilestone.objects.select_related("payment_tracking").all()
        ser = ProjectPaymentMilestoneSerializer(qs, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = ProjectPaymentMilestoneSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)

        # fetch payment instance
        payment = ProjectPaymentTracking.objects.get(pk=ser.validated_data["payment_tracking"].id) if hasattr(ser.validated_data["payment_tracking"], "id") else ProjectPaymentTracking.objects.get(pk=ser.validated_data["payment_tracking"])
        validated = ser.validated_data.copy()
        validated["payment_tracking"] = payment
        m = create_milestone(validated, request.user, enforce_budget=True)
        # notify stakeholders (example recipients)
        notify_milestone_update(m, [payment.created_by.email] if payment.created_by else [])
        return Response(ProjectPaymentMilestoneSerializer(m).data, status=status.HTTP_201_CREATED)


class MilestoneDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]    

    def get(self, request, pk):
        m = ProjectPaymentMilestone.objects.get(pk=pk)
        return Response(ProjectPaymentMilestoneSerializer(m).data)

    # def patch(self, request, pk):
    #     ser = ProjectPaymentMilestoneSerializer(instance=ProjectPaymentMilestone.objects.get(pk=pk), data=request.data, partial=True, context={"request": request})
    #     ser.is_valid(raise_exception=True)
    #     m = update_milestone(pk, ser.validated_data, request.user)
    #     notify_milestone_update(m, [m.payment_tracking.created_by.email] if m.payment_tracking.created_by else [])
    #     return Response(ProjectPaymentMilestoneSerializer(m).data)
    def put(self, request, pk):
        milestone = ProjectPaymentMilestone.objects.get(pk=pk)
        milestone.status = request.data.get("status", milestone.status)
        milestone.notes = request.data.get("notes", milestone.notes)
        milestone.save()
        notify_milestone_update(milestone)
        return Response({"msg": "Milestone updated"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        ProjectPaymentMilestone.objects.get(pk=pk).delete()
        return Response({"detail": "Deleted"}, status=status.HTTP_204_NO_CONTENT)


# Transactions
class TransactionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]    

    def post(self, request):
        ser = PaymentTransactionSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        payment_id = ser.validated_data["payment_tracking"].id if hasattr(ser.validated_data["payment_tracking"], "id") else ser.validated_data["payment_tracking"]
        tx = create_transaction(payment_id, ser.validated_data["amount"], request.user, method=ser.validated_data.get("method"), notes=ser.validated_data.get("notes"))
        payment = ProjectPaymentTracking.objects.get(pk=payment_id)
        # If budget breach after transaction, notify
        if payment.is_budget_exceeded:
            notify_budget_breach(payment, [payment.created_by.email] if payment.created_by else [])
        return Response(PaymentTransactionSerializer(tx).data, status=status.HTTP_201_CREATED)


# Additional budget (requests & approvals)
class AdditionalRequestListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        qs = AdditionalBudgetRequest.objects.select_related("payment_tracking").all()
        ser = AdditionalBudgetRequestSerializer(qs, many=True)
        return Response(ser.data)

    # def post(self, request):
    #     ser = AdditionalBudgetRequestSerializer(data=request.data, context={"request": request})
    #     ser.is_valid(raise_exception=True)
    #     payment_id = ser.validated_data["payment_tracking"].id if hasattr(ser.validated_data["payment_tracking"], "id") else ser.validated_data["payment_tracking"]
    #     req = request_additional(payment_id, ser.validated_data["requested_amount"], ser.validated_data.get("reason"), request.user)
    #     # notify approvers (example)
    #     notify_budget_request(req, ["finance@company.com"])
    #     return Response(AdditionalBudgetRequestSerializer(req).data, status=status.HTTP_201_CREATED)

    def post(self, request):
        # create budget request
        req = AdditionalBudgetRequest.objects.create(
            payment_tracking_id=request.data["payment_tracking"],
            requested_amount=request.data["requested_amount"],
            reason=request.data.get("reason", ""),
            created_by=request.user,
        )
        # send email
        notify_budget_request(req)
        return Response({"msg": "Budget request created"}, status=status.HTTP_201_CREATED)

from .services import notify_budget_approval, notify_budget_rejection


class AdditionalRequestApproveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsFinanceApprover]
    authentication_classes = [JWTAuthentication]    

    # def post(self, request, req_id):
    #     notes = request.data.get("approval_notes", "")
    #     req = approve_request(req_id, request.user, notes)
    #     notify_budget_approved(req, [req.created_by.email] if req.created_by else [])
    #     return Response(AdditionalBudgetRequestSerializer(req).data)
    def post(self, request, pk):
        req = AdditionalBudgetRequest.objects.get(pk=pk)
        action = request.data.get("action")  # "approve" or "reject"

        if action == "approve":
            req.status = "Approved"
            req.approved_by = request.user
            req.save()
            notify_budget_approval(req)
        else:
            req.status = "Rejected"
            req.approved_by = request.user
            req.save()
            notify_budget_rejection(req)

        return Response({"msg": f"Budget {action}d"}, status=status.HTTP_200_OK)

    # def delete(self, request, req_id):
    #     notes = request.data.get("approval_notes", "")
    #     req = reject_request(req_id, request.user, notes)
    #     notify_budget_rejected(req, [req.created_by.email] if req.created_by else [])
    #     return Response(AdditionalBudgetRequestSerializer(req).data)


# Notifications & Rules
class NotificationListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        qs = Notification.objects.filter(recipient=request.user)
        ser = NotificationSerializer(qs, many=True)
        return Response(ser.data)


class RuleListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # add role-based permission for admin in production
    authentication_classes = [JWTAuthentication]    

    def get(self, request):
        qs = Rule.objects.all()
        ser = RuleSerializer(qs, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = RuleSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        r = ser.save()
        return Response(RuleSerializer(r).data, status=status.HTTP_201_CREATED)
