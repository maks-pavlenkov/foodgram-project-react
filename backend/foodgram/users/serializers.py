from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from recipies.models import Following


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Имя пользователя занято'
        )]
    )
    first_name = serializers.CharField(
        required=True
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Email занят'
        )]
    )
    is_subscribed = serializers.SerializerMethodField(
        'get_sub',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_sub(self, obj):
        try:
            if self.context['request'].user.is_anonymous:
                return False
            return Following.objects.filter(
                user=obj,
                following=self.context['request'].user
            ).exists()
        except Exception:
            return False


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Имя пользователя занято'
        )]
    )
    first_name = serializers.CharField(
        required=True,
    )

    last_name = serializers.CharField(
        required=True,
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Email занят'
        )]
    )

    password = serializers.CharField(
        required=True,
    )

    def create(self, validated_data):
        instance = super().create(validated_data)
        passwd = validated_data.pop('password')
        instance.set_password(passwd)
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = UserSerializer(instance)
        return serializer.data

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class TokenSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=254, required=True)
    password = serializers.CharField(max_length=150, required=True)


class NewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150, required=True)
    current_password = serializers.CharField(max_length=150, required=True)
