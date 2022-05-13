from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'PATCH':
            user = self.context['view'].get_object()
            role = user.role
            print(role)
            if role == 'admin' or role != 'user' or role != 'moderator':
                raise ValidationError('АТАТА')
            return attrs
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',)
