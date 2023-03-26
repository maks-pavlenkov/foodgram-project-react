from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from recipies.models import Following, Recipe


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

    def validate(self, data):
        password = data['password']
        user = self.context.get('user')
        if user.check_password(password):
            return data
        raise serializers.ValidationError('Wrong password')


class NewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150, required=True)
    current_password = serializers.CharField(max_length=150, required=True)

    def create(self, validated_data):
        current_password = validated_data['current_password']
        new_password = validated_data['new_password']
        user = self.context['request'].user
        if not user.check_password(current_password):
            raise serializers.ValidationError('Неверный пароль!')
        user.set_password(new_password)
        user.save()
        return validated_data


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionsSerializer(serializers.ModelSerializer):
    recipes = RecipeSubscriptionSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email',
            'username', 'is_subscribed', 'recipes'
        )

    def get_is_subscribed(self, obj):
        return Following.objects.filter(
            user=self.context['request'].user,
            following=obj
        ).exists()


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = RecipeSubscriptionSerializer(many=True, required=False)

    username = serializers.SerializerMethodField('get_username')
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')
    email = serializers.SerializerMethodField('get_email')
    recipes = RecipeSubscriptionSerializer(
        many=True, required=False, read_only=True
    )

    class Meta:
        model = Following
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'recipes'
        )

    def create(self, validated_data):
        user = validated_data.get('user', False)
        following = validated_data.get('following', False)
        if not following:
            raise serializers.ValidationError('Failed: No such user')
        if user == following:
            raise serializers.ValidationError(
                'Failed: You cant follow yourself!'
            )
        if Following.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                f'Failed: You already follow {following.username}'
            )
        return Following.objects.create(**validated_data)

    def get_username(self, obj):
        return obj.following.username

    def get_first_name(self, obj):
        return obj.following.first_name

    def get_last_name(self, obj):
        return obj.following.last_name

    def get_email(self, obj):
        return obj.following.email
