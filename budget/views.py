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
from .models import Estimation
from .serializers import EstimationSerializer
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType
from .models import Document, validate_file
# Create your views here.
    
class EstimationCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = EstimationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(created_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Duplicate estimation"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        estimations = Estimation.objects.all()
        serializer = EstimationSerializer(estimations, many=True)
        return Response(serializer.data)    
 


class DocumentUploadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request, *args, **kwargs):
        try:
            content_type_id = request.data.get("content_type_id")  # Table reference
            object_id = request.data.get("object_id")  # Row ID
            file = request.FILES.get("file")
            description = request.data.get("description", "")

            if not content_type_id or not object_id or not file:
                return Response({"error": "content_type_id, object_id, and file are required."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Validate file size & extension
            validate_file(file)

            # Get ContentType instance
            try:
                content_type = ContentType.objects.get(id=content_type_id)
            except ContentType.DoesNotExist:
                return Response({"error": "Invalid content_type_id"}, status=status.HTTP_400_BAD_REQUEST)

            # Create Document instance
            doc = Document.objects.create(
                content_type=content_type,
                object_id=object_id,
                file=file,
                description=description,
                uploaded_by=request.user
            )

            return Response({
                "id": doc.id,
                "file": doc.file.url,
                "description": doc.description,
                "uploaded_at": doc.uploaded_at,
                "uploaded_by": doc.uploaded_by.username if doc.uploaded_by else None
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class DocumentListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        content_type_id = request.query_params.get("content_type_id")
        object_id = request.query_params.get("object_id")

        if not all([content_type_id, object_id]):
            return Response({"error": "content_type_id and object_id are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        documents = Document.objects.filter(
            content_type_id=content_type_id,
            object_id=object_id
        )
        data = [{
            "id": doc.id,
            "file": doc.file.url,
            "description": doc.description,
            "uploaded_at": doc.uploaded_at
        } for doc in documents]
        return Response(data, status=status.HTTP_200_OK)





    def delete(self, request, pk, *args, **kwargs):
        try:
            document = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)

        if document.uploaded_by != request.user:
            return Response({"error": "You can only delete your own files."},
                            status=status.HTTP_403_FORBIDDEN)

        document.file.delete(save=False)
        document.delete()
        return Response({"message": "Document deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
