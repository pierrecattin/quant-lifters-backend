from rest_framework import serializers
from django.contrib.auth.models import User
from trainer.models import *


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField() 
    
class CompactUserSerializer(serializers.Serializer):
    username = serializers.CharField()

class LifterSerializer(serializers.Serializer):
    username = CompactUserSerializer(source='user')

class BodypartSerializer(serializers.Serializer):
    name = serializers.CharField()

class ExerciseSerializer(serializers.Serializer):
    name = serializers.CharField()
    is_unilateral = serializers.BooleanField()
    primary_bodyparts = BodypartSerializer(many=True)
    secondary_bodyparts = BodypartSerializer(many=True)
    created_by = LifterSerializer()
    shared_with = LifterSerializer(many=True)

