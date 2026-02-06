from users.models import User
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from django.contrib.auth.password_validation import validate_password


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
        )

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError("Пользователь с такой почтой уже зарегистрирован.")
        return email

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # 🔥 вот тут магия
        user.is_active = False  # для активации по почте
        user.save()
        return user
