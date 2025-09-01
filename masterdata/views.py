from django.shortcuts import render

# Create your views here.
from .serializers import ModuleSerializer, MasterDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, MasterData
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated 

    
class CategoryView(APIView):
    permission_classes = [IsAuthenticated]  # Allow unrestricted access
    authentication_classes = [JWTAuthentication]  # Disable authentication for this view
    def get(self, request, module_id=None):
        if module_id:
            try:
                module = Category.objects.get(module_id=module_id)
                serializer = ModuleSerializer(module)
                return Response(serializer.data)
            except Category.DoesNotExist:
                return Response({"error": "Module not found"}, status=404)
        else:
            modules = Category.objects.all()
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
            module = Category.objects.get(module_id=module_id)
        except Category.DoesNotExist:
            return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModuleSerializer(module, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, module_id):
        try:
            module = Category.objects.get(module_id=module_id)
        except Category.DoesNotExist:
            return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

        module.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class MasterDataView(APIView):
    permission_classes = [IsAuthenticated]  # Allow unrestricted access    
    authentication_classes = [JWTAuthentication]  # Disable authentication for this view
    def get(self,request, resource_id=None):
        if resource_id:
            try:
                resource = MasterData.objects.get(id=resource_id)
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
            resource = MasterData.objects.get(id=resource_id)
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
        