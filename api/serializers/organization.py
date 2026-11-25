from importlib.metadata import MetadataPathFinder
from rest_framework.serializers import ModelSerializer
from organization.models import Branch, Organization


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "org_name",
            "org_logo",
            "tax_number",
            "website",
            "company_contact_number",
            "company_contact_email",
            "contact_person_number",
            "company_address",
            "company_bank_qr",
            "current_fiscal_year",
            "allow_negative_sales"
        ]


class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        # fields = [
        #     "id",
        #     "name",
        #     "address",
        #     "contact_number",
        #     "branch_manager",
        #     "organization",
        #     "branch_code",
        # ]
        fields = "__all__"  # keep whatever you already have

    def validate(self, attrs):
        if self.instance is None and Branch.objects.active().exists():
            raise serializers.ValidationError(
                "Only one branch is allowed. A branch already exists."
            )
        return attrs
        
from rest_framework import serializers
from organization.models import PrinterSetting
class PrinterSettingSerializer(ModelSerializer):
    
    type = serializers.SerializerMethodField()

    class Meta:
        model = PrinterSetting
        fields = "url", "port", "ip", "type", "print_status"
    
    def get_type(self, obj):
        return obj.printer_location
