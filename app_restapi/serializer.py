from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import UserRegistration


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        print(token)
        # Add custom claims
        token['email'] = user.email
        return token


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'username', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = make_password(validated_data.pop('password'))
        return User.objects.create(password=password,
                                   **validated_data)


class userSerializer(serializers.ModelSerializer):
    # user = CreateUserSerializer(required=True)

    class Meta:
        model = UserRegistration
        fields = ['phonenumber','user_role','emirates_id','emirates_office','gender'
                  ,'qualification','university','year_passed_out','skills','exp_years'
                  ,'designation','work_company','employee_count','auth_name','user','about_company','industry_type']

    # def create(self, validated_data):
    #     # print(validated_data.pop('user'))
    #     user_data = validated_data.pop('user')
    #     print(user_data)
    #     user = CreateUserSerializer.create(CreateUserSerializer(),
    #                                        validated_data=user_data)
    #     print(user.id)
    #     print()
    #     user_register, created = UserRegistration.objects.update_or_create(
    #         user=user, **validated_data)
    #     return user_register



