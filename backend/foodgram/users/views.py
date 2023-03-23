from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipies.models import Following
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from api.permissions import RecipeFavShopFollowPermission
from .permissions import UsersPermission
from .serializers import (NewPasswordSerializer, SubscribeSerializer,
                          SubscriptionsSerializer, TokenSerializer,
                          UserCreateSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (UsersPermission,)
    queryset = User.objects.all()
    http_method_names = ('get', 'post', 'head')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return UserSerializer
        return UserCreateSerializer

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_login(request):
    email = request.data['email']
    user = get_object_or_404(User, email=email)
    serializer = TokenSerializer(
        data=request.data,
        context={
            'user': user
        }
    )
    if serializer.is_valid(raise_exception=True):
        token = str(RefreshToken.for_user(user).access_token)
        return Response(
            {"auth_token": token},
            status=status.HTTP_201_CREATED
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
    serializer = NewPasswordSerializer(
        data=request.data,
        context={
            'request': request
        })
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class SubscriptionsViewSet(ReadOnlyModelViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = [RecipeFavShopFollowPermission]
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        authors = self.request.user.follower.all()
        authors_pk = [author.following.pk for author in authors]
        queryset = User.objects.filter(pk__in=authors_pk)
        return queryset


class Subscribe(APIView):
    permission_classes = [RecipeFavShopFollowPermission]
    filter_backends = (DjangoFilterBackend,)

    def get_object(self, pk):
        return Following.objects.get(following=pk)

    def post(self, request, pk):
        following = get_object_or_404(User, id=pk)
        request.data['user'] = self.request.user
        request.data['following'] = following
        serializer = SubscribeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(**request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Подскажи, почему это костыль? и как сделать правильнее?()
        # Почти точно такой же код, с обработкой 400 ошибок, был в теории, поэтому это ставит меня в тупик)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        following = self.get_object(pk)
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
