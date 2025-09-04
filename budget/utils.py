from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

def custom_exception_handler(exc, context):
    # Convert Django ValidationError to DRF ValidationError for consistent JSON
    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(detail=exc.message_dict if hasattr(exc, "message_dict") else exc.messages)
    response = exception_handler(exc, context)
    if response is None:
        # fallback
        return Response({"error": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
