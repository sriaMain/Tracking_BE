from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ProjectEstimation, ProjectPaymentTracking, ProjectPaymentMilestone, PaymentTransaction, AdditionalBudgetRequest, Notification, Rule, PaymentHistory, AuditLog, Hold
from django.core.exceptions import ValidationError  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ProjectPaymentTrackingSerializer, ProjectPaymentMilestoneSerializer,EstimationSerializer,
    PaymentTransactionSerializer, AdditionalBudgetRequestSerializer, NotificationSerializer, RuleSerializer,ProjectPaymentTrackingUpdateSerializer, HoldSerializer, ProfitLossSerializer
)

from .services import create_payment, update_payment, get_payment
from .services import create_milestone
from .services import create_transaction
from .services import request_additional, approve_request, reject_request
from .services import evaluate_and_notify
from .permission import IsFinanceApprover
from .services import notify_budget_request,  notify_milestone_update, notify_budget_breach, calculate_project_profit_loss
from django.utils import timezone
import traceback
from decimal import Decimal
from django.db import models
from django.db.models import Sum


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
    def get(self, request, pk):
        estimation = get_object_or_404(ProjectEstimation, pk=pk)
        serializer = EstimationSerializer(estimation)
        return Response(serializer.data)

    


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


    

class ProfitLossAdvancedAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, pk):
        data = calculate_project_profit_loss(pk)
        serializer = ProfitLossSerializer(instance=data)
        return Response(serializer.data)


class ProjectEstimationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
    Fetch latest estimation for a given project.
    """
    
    def get(self, request, pk, format=None):
            estimation = ProjectEstimation.objects.filter(project_id=pk).last()
            if not estimation:
                return Response(
                    {"error": "No estimation found for this project."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = EstimationSerializer(estimation)
            return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectPaymentTrackingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
    Fetch all payment tracking and milestones for a given project.
    """

    def get(self, request, pk, format=None):
        try:
            payments = ProjectPaymentTracking.objects.filter(project_id=pk).order_by("-created_at")
            if not payments.exists():
                return Response({"error": "No payments found for this project."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProjectPaymentTrackingSerializer(payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("❌ ERROR:", e)
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   


class ProjectEstimationPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk, format=None):
        # --- Latest estimation ---
        estimation = ProjectEstimation.objects.filter(project_id=pk).last()
        if estimation:
            estimation_data = {
                "id": estimation.id,
                "estimation_date": estimation.estimation_date,
                "estimation_provider": str(estimation.estimation_provider) if estimation.estimation_provider else None,
                "estimation_review": str(estimation.estimation_review) if estimation.estimation_review else None,
                "initial_estimation_amount": estimation.initial_estimation_amount,
                "approved_estimation": estimation.approved_amount,
                "purchase_order_status": estimation.purchase_order_status,
                "created_at": estimation.created_at,
                "modified_at": estimation.modified_at,
                "created_by": estimation.created_by.id if estimation.created_by else None,
                "modified_by": estimation.modified_by.id if estimation.modified_by else None,
            }
        else:
            estimation_data = None

        # --- Payment tracking ---
        payments = ProjectPaymentTracking.objects.filter(project_id=pk)
        payment_list = []

        for payment in payments:
            milestones = payment.milestones.all() if hasattr(payment, "milestones") else []
            milestone_list = [
                {"id": m.id, "name": m.name, "amount": m.amount, "due_date": m.due_date}
                for m in milestones
            ]

            active_holds = payment.holds.filter(is_active=True) if hasattr(payment, "holds") else []
            total_hold_amount = active_holds.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
            holds_list = [
                {"id": h.id, "amount": h.amount, "is_active": h.is_active, "created_at": h.created_at, "released_at": h.released_at}
                for h in payment.holds.all()
            ]

            payment_list.append({
                "id": payment.id,
                "payment_type": payment.payment_type,
                "other_payment_type": getattr(payment, "other_payment_type", None),  # safe fallback
                "approved_budget": payment.approved_budget,
                "additional_amount": payment.additional_amount,
                "payout": payment.payout,
                "retention_amount": payment.retention_amount,
                "penalty_amount": payment.penalty_amount,
                "total_available_budget": payment.total_available_budget,
                "total_milestones_amount": payment.total_milestones_amount,
                "completed_milestones_amount": payment.completed_milestones_amount,
                "pending": payment.pending,
                "total_hold_amount": total_hold_amount,
                "holds": holds_list,
                "created_at": payment.created_at,
                "modified_at": payment.modified_at,
                "created_by": payment.created_by.id if payment.created_by else None,
                "modified_by": payment.modified_by.id if payment.modified_by else None,
                "milestones": milestone_list,
            })

        return Response({"estimation": estimation_data, "payments": payment_list}, status=status.HTTP_200_OK)





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
        
    def put(self, request, pk):
        serializer = ProjectPaymentTrackingUpdateSerializer(
            instance=self.get_object(pk),
            data=request.data,
            partial=False,   # full update
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        updated_instance = update_payment(pk, serializer.validated_data, request.user)
        return Response(ProjectPaymentTrackingSerializer(updated_instance).data)
    
 


    def delete(self, request, pk):
        obj = get_payment(pk)
        obj.delete()
        return Response({"detail": "Deleted"}, status=status.HTTP_204_NO_CONTENT)

class AddHoldView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk):
        try:
            project = ProjectPaymentTracking.objects.get(id=pk)
        except ProjectPaymentTracking.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        from decimal import Decimal, InvalidOperation
        try:
            amount = Decimal(str(request.data.get("amount", "0.00")))
        except (InvalidOperation, TypeError):
            return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= 0:
            return Response({"error": "Invalid hold amount"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if hold exceeds pending budget
        active_holds_sum = project.holds.filter(is_active=True).aggregate(total=models.Sum('amount'))['total'] or Decimal("0.00")
        pending_budget = (
            project.total_available_budget
            - (project.payout or Decimal("0.00"))
            - active_holds_sum
            - (project.retention_amount or Decimal("0.00"))
            + (project.penalty_amount or Decimal("0.00"))
        )
        if amount > pending_budget:
            return Response({"error": "Hold amount exceeds pending budget"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the hold
        hold = Hold.objects.create(project=project, amount=amount, is_active=True)
        serializer = HoldSerializer(hold)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReleaseHoldView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]    

    def post(self, request, hold_id):
        try:
            hold = Hold.objects.get(id=hold_id, is_active=True)
        except Hold.DoesNotExist:
            return Response({"error": "Hold not found or already released"}, status=status.HTTP_404_NOT_FOUND)

        hold.is_active = False
        hold.released_at = timezone.now()
        hold.save()
        serializer = HoldSerializer(hold)
        return Response(serializer.data, status=status.HTTP_200_OK)
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


    def post(self, request, req_id, *args, **kwargs):
        try:
            additional_request = AdditionalBudgetRequest.objects.get(id=req_id)

            if additional_request.status != AdditionalBudgetRequest.STATUS_PENDING:
                return Response({"error": "Request is already processed"}, status=400)

            # Approve the request
            additional_request.status = AdditionalBudgetRequest.STATUS_APPROVED
            additional_request.approved_by = request.user
            additional_request.approved_at = timezone.now()
            additional_request.approval_notes = request.data.get("approval_notes", "")
            additional_request.save()

            # Update only the additional_amount
            payment = additional_request.payment_tracking
            payment.additional_amount += additional_request.requested_amount
            payment.save()  # total_available_budget is automatically updated via the property

            return Response({"message": "Request approved successfully"})
        except AdditionalBudgetRequest.DoesNotExist:
            return Response({"error": "Request not found"}, status=404)

  
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
