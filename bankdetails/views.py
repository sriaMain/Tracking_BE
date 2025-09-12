
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import BankDetails
from .serializers import BankDetailsSerializer


class BankDetailsListCreateAPIView(APIView):
    """
    Handle listing all bank accounts and creating a new one.
    """

    def get(self, request):
        bank_details = BankDetails.objects.all()
        serializer = BankDetailsSerializer(bank_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankDetailsRetrieveUpdateDestroyAPIView(APIView):
    """
    Handle retrieving, updating, and deleting a specific bank account.
    """

    def get_object(self, pk):
        return get_object_or_404(BankDetails, pk=pk)

    def get(self, request, pk):
        bank_detail = self.get_object(pk)
        serializer = BankDetailsSerializer(bank_detail)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        bank_detail = self.get_object(pk)
        serializer = BankDetailsSerializer(bank_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bank_detail = self.get_object(pk)
        bank_detail.delete()
        return Response({"message": "Bank detail deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
