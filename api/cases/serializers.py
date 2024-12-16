from rest_framework import serializers
from api.cases.models import Cases

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cases
        fields = ['case_id', 'title', 'client_id', 'created_by','lawyer_id', 'user_id','case_type', 'description', 'is_anonymous', 'status']
