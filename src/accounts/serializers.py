from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "password2",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Password doesn't matched")
        data.pop("password2")
        return data

    def save(self, **kwargs):
        password = self.validated_data.pop("password")

        user = User(**self.validated_data, **kwargs)
        user.set_password(password)
        user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False, write_only=True
    )
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "avatar"]
        extra_kwargs = {"email": {"read_only": True}}


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirm_password = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    class Meta:
        model = User
        fields = ["old_password", "new_password", "confirm_password"]

    def save(self, **kwargs):
        user: User = self.instance
        if user.check_password(self.validated_data["old_password"]):
            if (
                self.validated_data["new_password"]
                == self.validated_data["confirm_password"]
            ):
                user.set_password(self.validated_data["new_password"])
                user.save()
                return user

            raise serializers.ValidationError(
                {"confirm_password": "Password does not match"}
            )

        raise serializers.ValidationError({"old_password": "Wrong password"})
