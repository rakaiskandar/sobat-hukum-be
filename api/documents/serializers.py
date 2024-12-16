from rest_framework import serializers
from api.documents.models import Documents
from api.cases.models import Cases  # Import Case model for validation

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ['document_id', 'case_id', 'file_name', 'file_path', 'uploaded_at']
        read_only_fields = ['document_id', 'uploaded_at']  # Mark non-writable fields

    def validate_case_id(self, value):
        # Validate if the case ID exists
        if not Cases.objects.filter(case_id=value).exists():
            raise serializers.ValidationError("The case_id provided does not exist.")
        return value

    def validate_file_path(self, value):
        # Validate file size and type
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("File size must be under 5MB.")
        if not value.name.endswith(('.png', '.jpg', '.pdf', '.docx')):  # Allowed types
            raise serializers.ValidationError("Unsupported file type.")
        return value
