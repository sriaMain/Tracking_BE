


from rest_framework import serializers
from .models import BankDetails
from organization.models import Organisation
from project_creation.models import Client
from users.models import MasterData


class BankDetailsSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(read_only=True, slug_field='username')
    modified_by = serializers.SlugRelatedField(read_only=True, slug_field='username')
    # modified_by = serializers.StringRelatedField(read_only=True)
    organisation = serializers.SlugRelatedField(
        slug_field="organisation_name", queryset=Organisation.objects.all(), required=False, allow_null=True
    )
    client = serializers.SlugRelatedField(
        slug_field="Client_company", queryset=Client.objects.all(), required=False, allow_null=True
    )
    # resource = serializers.SlugRelatedField(
    #     slug_field="name_of_resource", queryset=MasterData.objects.all(), required=False, allow_null=True
    # )
    # resource = serializers.SlugRelatedField(
    #     slug_field="__str__",  # calls MasterData.__str__ which returns string
    #     queryset=MasterData.objects.all(),
    #     required=False,
    #     allow_null=True
    # )

    # resource = serializers.StringRelatedField()
    resource = serializers.SlugRelatedField(
        slug_field="id",  # Use the MasterData ID
        queryset=MasterData.objects.all(),
        required=False,
        allow_null=True
    )


    class Meta:
        model = BankDetails
        fields = "__all__"
        # exclude = ['created_by', 'modified_by'] 

    def validate(self, data):
        owners = [bool(data.get("organisation")), bool(data.get("client")), bool(data.get("resource"))]
        if owners.count(True) != 1:
            raise serializers.ValidationError("BankDetails must belong to exactly one of: Organisation, Client, or Resource.")
        return data
