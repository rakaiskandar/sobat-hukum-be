from rest_framework import serializers
from api.cases.models import Cases
from django.contrib.auth.models import User

class CaseSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = Cases
        fields = [
            'case_id', 'title', 'client_id', 'created_at', 'created_by',
            'lawyer_id', 'user_id', 'case_type', 'description', 
            'is_anonymous', 'status', 'phone_number'
        ]

    def get_phone_number(self, obj):
        # Pastikan user_id tidak null
        if obj.user_id:
            return obj.user_id.phone_number
        return None
