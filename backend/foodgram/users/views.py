from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import UsersPermission
from .serializers import (NewPasswordSerializer, TokenSerializer,
                          UserCreateSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (UsersPermission,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return UserSerializer
        return UserCreateSerializer

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        instance = request.user
        print(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_login(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')
    user = get_object_or_404(User, email=email)
    if user:
        if user.check_password(password):
            token = str(RefreshToken.for_user(user).access_token)
            return Response(
                {"auth_token": token},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                'Invalid password',
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            'No such email',
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def token_logout(request):
    logout(request)
    RefreshToken.for_user(request.user).access_token
    return Response('OK', status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    print('CHANGE PASSWORD _)(_+)(*+)(*)(*_)(*')
    serializer = NewPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    password = serializer.validated_data.get('current_password')
    new_password = serializer.validated_data.get('new_password')
    if password:
        if request.user.check_password(password):
            request.user.set_password(new_password)
            return Response(
                'Пароль успешно изменен',
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                'Неверный пароль',
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            'Введите текущий пароль',
            status=status.HTTP_400_BAD_REQUEST
        )
