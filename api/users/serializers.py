from rest_framework import serializers
from api.users.models import Users, Lawyers, Clients
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=Users.ROLE_CHOICES, default='client')

    class Meta:
        model = Users
        fields = ['name', 'username', 'email', 'password', 'role', 'phone_number']

    def create(self, validated_data):
        user = Users.objects.create_user(
            name=validated_data['name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            phone_number=validated_data['phone_number'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password")

        data["user"] = user
        return data
    
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['nik', 'is_verified']

class LawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyers
        fields = ['license_number', 'specialization', 'experience_years', 'availability', 'is_verified']