from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import AdminOrSuperuser
from .models import User
from .serializers import UserAuthSerializer
from .serializers import UserSignUpSerializer, UserCreateSerializer


@api_view(['POST'])
def signup(request):
    serializer = UserSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if request.data['username'] == 'me':
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            exception=True
        )
    user, created = User.objects.get_or_create(
        email=request.data.get('email'),
        username=request.data.get('username')
    )
    verify_code = default_token_generator.make_token(user)
    email = EmailMessage(
        'YaMDB registration',
        f'Your verification code: {verify_code}',
        'no-reply@yamdb.com',
        [request.data['email']],
    )
    email.send()
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_token(request):
    try:
        username, confirmation_code = request.data.values()
    except ValueError as err:
        return Response(
            {"Ошибка": f"{err}"}, status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, username=username)
    serializer = UserAuthSerializer(user, data=request.data)
    serializer.is_valid(raise_exception=True)
    if not default_token_generator.check_token(user, confirmation_code):
        raise ValidationError("Неверный confirmation_code")
    user.is_active = True
    user.save()
    return Response(
        {"Ваш токен": f"{AccessToken.for_user(user)}"},
        status=status.HTTP_200_OK,
    )


class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (IsAuthenticated, AdminOrSuperuser)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['get'], detail=True, url_path='me')
    def get_object(self):
        if self.kwargs.get('username') == 'me':
            self.permission_classes = (IsAuthenticated, )
            return self.request.user
        return super(UserCreateViewSet, self).get_object()
