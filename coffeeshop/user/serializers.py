from django.contrib.auth import password_validation, authenticate
from knox.models import AuthToken
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import clean_existing_user_values


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(label="Token", read_only=True)
    confirm_password = serializers.CharField(
        label=_("Confirm Password"), max_length=100, write_only=True
    )
    current_password = serializers.CharField(
        label=_("Current Password"), max_length=100, write_only=True, required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "current_password",
            "token",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "email": {"required": True}
        }

    def validate_password(self, value):
        password_validation.validate_password(value, user=self.context.get("user"))
        return value

    def validate(self, attrs):
        # validate username
        clean_existing_user_values(
            query_param={"username": attrs.get("username")},
            instance=self.instance,
            validation_class=serializers.ValidationError,
        )

        # validate email
        clean_existing_user_values(
            query_param={"email": attrs.get("email")},
            instance=self.instance,
            validation_class=serializers.ValidationError,
        )

        if not self.instance:
            password = attrs.get("password", None)
            confirm_password = attrs.pop("confirm_password", None)
            if password and confirm_password:
                if password != confirm_password:
                    raise serializers.ValidationError(
                        {
                            "confirm_password": [
                                _("password and confirm_password does not match")
                            ]
                        }
                    )
            else:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            _(
                                "Please provide both password and "
                                "confirm_password fields"
                            )
                        ]
                    }
                )

        return super(UserSerializer, self).validate(attrs)

    def get_token(self, obj):
        _, token = AuthToken.objects.create(user=obj)

        return token

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        # change password
        password = validated_data.pop("password", None)
        current_password = validated_data.get("current_password", None)

        if password:
            if current_password:
                if password == current_password:
                    raise serializers.ValidationError(
                        {
                            "password": [
                                _(
                                    "The Current password and New Password must not be same"
                                )
                            ]
                        }
                    )
                if not instance.check_password(current_password):
                    raise serializers.ValidationError(
                        {"current_password": [_("Current password is invalid")]}
                    )
            else:
                raise serializers.ValidationError(
                    {"current_password": [_("Please provide Current password")]}
                )

            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                raise serializers.ValidationError(detail="Account is not active.")
        else:
            raise serializers.ValidationError(
                detail="Invalid username/password. Please try again!"
            )

        _, token = AuthToken.objects.create(user=user)

        return {"token": token, "user_id": user.id}
