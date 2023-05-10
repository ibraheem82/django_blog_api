from rest_framework import serializers
from django.contrib.auth.models import User
class RegisterSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()


  def validate(self, data):
    if User.object.filter(username = data('username')).exists():
      raise serializer.ValidationError('Username already exists')
    return data