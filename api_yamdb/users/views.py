import random

from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, filters, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import AdminOrSuperuser
from .models import User
from .serializers import UserSignUpSerializer, UserCreateSerializer
from .serializers import UserSerializer, UserAuthSerializer


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def send_mail(self, request):
        email = EmailMessage(
            'YaMDB registration',
            f'Your verification code: {random.randint(1000, 9999)}',
            'no-reply@yamdb.com',
            [request.data['email']],
        )
        return email.send()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data['username'] == 'me':
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                exception=True
            )
        self.perform_create(serializer)
        self.send_mail(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAuthSerializer

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'access': str(refresh.access_token),
        }

    def perform_create(self, serializer):
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        if user:
            return Response(self.get_tokens_for_user(user))


class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (IsAuthenticated, AdminOrSuperuser)
    authentication_classes = [JWTAuthentication, ]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    #def partial_update(self, request, *args, **kwargs):
    #    kwargs['partial'] = True
    #    user = self.request.user
    #    if user.role == 'admin':
    #        serializer = self.get_serializer(data=request.data)
    #        if not serializer.is_valid():
    #            return Response(status=status.HTTP_400_BAD_REQUEST)
    #    return self.update(request, *args, **kwargs)


class CurrentUserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        pass
