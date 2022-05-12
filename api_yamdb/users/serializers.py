from rest_framework import serializers

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
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, attrs):
        user = self.context['request'].user
        if user.role == 'admin':
            user.is_staff = True
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


# class UserAuthSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = User
#        fields = ('username', 'confirmation_code')
#               !!! пока не реализовано !!!
