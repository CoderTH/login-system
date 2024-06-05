from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=3, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
