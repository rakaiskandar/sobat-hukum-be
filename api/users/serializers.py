from rest_framework import serializers
from api.users.models import Users, Lawyers, Clients
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=Users.ROLE_CHOICES, default='client')

    class Meta:
        model = Users
        fields = ['name', 'username', 'age', 'gender', 'email', 'password', 'role', 'phone_number']

    def create(self, validated_data):
        user = Users.objects.create_user(
            name=validated_data['name'],
            username=validated_data['username'],
            age=validated_data['age'],
            gender=validated_data['gender'],
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
        fields = ['user', 'nik', 'is_verified']

class LawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyers
        fields = ['user', 'license_number', 'specialization', 'experience_years', 'availability', 'is_verified']
        
class UserSerializer(serializers.ModelSerializer):
    is_verified = serializers.BooleanField(read_only=True)  # Make it read-only
    
    class Meta:
        model = Users
        fields = ['user_id', 'name', 'username', 'profile_picture', 'email', 'phone_number', 'age', 'gender', 'role', 'is_verified']

    def get_is_verified(self, obj):
        # We assume `obj` is the `Users` instance. Now we use the dynamic logic
        if obj.role == 'client':
            return obj.client.is_verified if obj.client else False
        elif obj.role == 'lawyer':
            return obj.lawyer.is_verified if obj.lawyer else False
        return False
    
class UpdateClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ["nik"]

class UpdateLawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyers
        fields = ["license_number", "specialization", "experience_years"]

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["name", "usernmae", "email", "phone_number", "age", "gender", "profile_picture"]

    def validate_email(self, value):
        if Users.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_phone_number(self, value):
        if Users.objects.exclude(pk=self.instance.pk).filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value
