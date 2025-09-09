from django.shortcuts import render

# Create your views here.
from .serializers import ModuleSerializer, MasterDataSerializer, ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Module, MasterData
from authentication.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

class ModuleView(APIView):
    def get(self, request, module_id=None):
        if module_id:
            try:
                module = Module.objects.get(module_id=module_id)
                serializer = ModuleSerializer(module)
                return Response(serializer.data)
            except Module.DoesNotExist:
                return Response({"error": "Module not found"}, status=404)
        else:
            modules = Module.objects.all()
            serializer = ModuleSerializer(modules, many=True)
            return Response(serializer.data)

    
    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, module_id):
        try:
            module = Module.objects.get(module_id=module_id)
        except Module.DoesNotExist:
            return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModuleSerializer(module, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, module_id):
        try:
            module = Module.objects.get(module_id=module_id)
        except Module.DoesNotExist:
            return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

        module.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class MasterDataView(APIView):
    def get(self,request, resource_id=None):
        if resource_id:
            try:
                resource = MasterData.objects.get(name_of_resource_id=resource_id)
                serializer = MasterDataSerializer(resource)
                return Response(serializer.data)
            except MasterData.DoesNotExist:
                return Response({"error": "Resource not found"}, status=404)
        else:
            resources = MasterData.objects.all()
            serializer = MasterDataSerializer(resources, many=True)
            return Response(serializer.data)
        
    def post(self, request):
        serializer = MasterDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, resource_id):
        try:
            resource = MasterData.objects.get(name_of_resource_id=resource_id)
        except MasterData.DoesNotExist:
            return Response({"error": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MasterDataSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, resource_id):
        try:
            resource = MasterData.objects.get(name_of_resource_id=resource_id)
        except MasterData.DoesNotExist:
            return Response({"error": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MasterDataSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, resource_id):
        try:
            resource = MasterData.objects.get(id=resource_id)
        except MasterData.DoesNotExist:
            return Response({"error": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

        resource.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModuleUsersView(APIView):
    def get(self, request, module_id):
        master_records = MasterData.objects.filter(module_id=module_id).select_related("name_of_resource")
        users = [record.name_of_resource for record in master_records if record.name_of_resource]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes  = [JWTAuthentication]
    # permission_classes = [AllowAny]

    def get(self, request):
        """Get logged-in user's profile"""
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ResourceTypeAPIView(APIView):
    def get(self, request):
        values = [value for key, value in MasterData.RESOURCE_TYPE_CHOICES]
        return Response(values)

class WorkTypeAPIView(APIView):
    def get(self, request):
        values = [value for key, value in MasterData.WORK_TYPE_CHOICES]
        return Response(values)