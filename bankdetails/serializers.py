# from rest_framework import serializers
# from django.contrib.contenttypes.models import ContentType
# from .models import BankDetails




# class BankDetailSerializer(serializers.ModelSerializer):
#     content_type = serializers.CharField(write_only=True)  # "organisation", "client", "resource"

#     class Meta:
#         model = BankDetails
#         fields = ["id", "account_number", "ifsc_code", "bank_name", "content_type", "object_id"]

#     def create(self, validated_data):
#         content_type_name = validated_data.pop("content_type")
#         try:
#             ct = ContentType.objects.get(model=content_type_name.lower())
#         except ContentType.DoesNotExist:
#             raise serializers.ValidationError({"content_type": "Invalid content type"})
#         validated_data["content_type"] = ct
#         return BankDetails.objects.create(**validated_data)

#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         rep["content_type"] = instance.content_type.model  # show model name
#         rep["related_object"] = str(instance.content_object)  # show related obj name
#         return rep



from rest_framework import serializers
from .models import BankDetails
from organization.models import Organisation
from project_creation.models import Client
from masterdata.models import MasterData


class BankDetailsSerializer(serializers.ModelSerializer):
    organisation = serializers.SlugRelatedField(
        slug_field="organisation_name", queryset=Organisation.objects.all(), required=False, allow_null=True
    )
    client = serializers.SlugRelatedField(
        slug_field="Client_company", queryset=Client.objects.all(), required=False, allow_null=True
    )
    resource = serializers.SlugRelatedField(
        slug_field="name_of_resource", queryset=MasterData.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = BankDetails
        fields = "__all__"

    def validate(self, data):
        owners = [bool(data.get("organisation")), bool(data.get("client")), bool(data.get("resource"))]
        if owners.count(True) != 1:
            raise serializers.ValidationError("BankDetails must belong to exactly one of: Organisation, Client, or Resource.")
        return data
