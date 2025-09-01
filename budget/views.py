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
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType

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




class ProjectPaymentTrackingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk=None):
        if pk:
            tracking = get_object_or_404(ProjectPaymentTracking, pk=pk)
            serializer = ProjectPaymentTrackingSerializer(tracking)
            return Response(serializer.data)
        else:
            tracking = ProjectPaymentTracking.objects.all()
            serializer = ProjectPaymentTrackingSerializer(tracking, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ProjectPaymentTrackingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        tracking = get_object_or_404(ProjectPaymentTracking, pk=pk)
        serializer = ProjectPaymentTrackingSerializer(tracking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tracking = get_object_or_404(ProjectPaymentTracking, pk=pk)
        tracking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------
# Payment Milestone APIs
# -------------------------------
class ProjectPaymentMilestoneAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk=None):
        if pk:
            milestone = get_object_or_404(ProjectPaymentMilestone, pk=pk)
            serializer = ProjectPaymentMilestoneSerializer(milestone)
            return Response(serializer.data)
        else:
            milestones = ProjectPaymentMilestone.objects.all()
            serializer = ProjectPaymentMilestoneSerializer(milestones, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ProjectPaymentMilestoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        milestone = get_object_or_404(ProjectPaymentMilestone, pk=pk)
        serializer = ProjectPaymentMilestoneSerializer(milestone, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        milestone = get_object_or_404(ProjectPaymentMilestone, pk=pk)
        milestone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
