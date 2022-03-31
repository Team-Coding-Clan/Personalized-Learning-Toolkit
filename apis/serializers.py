from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import connect


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

        user.save()

        return user


class ConnectSerializer(serializers.ModelSerializer):
    user_id = RegisterSerializer(many=False)  # many=False; one to one

    class Meta:
        model = connect
        # exclude = ('user_id',)
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `connect` instance, given the validated data.
        """
        user = self.context['request'].user
        info = connect.objects.create(
            user_id=user,
            **validated_data
        )
        return info

    def update(self, instance, validated_data):
        # update the instance
        instance.github = validated_data.get('github', instance.github)
        instance.known_skills = validated_data.get('known_skills', instance.known_skills)
        instance.skills_to_learn = validated_data.get('skills_to_learn', instance.skills_to_learn)

        instance.save()

        return instance
