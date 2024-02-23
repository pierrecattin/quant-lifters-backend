from rest_framework import serializers
from django.contrib.auth.models import User
from trainer.models import *


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField() 
    bodyweight = serializers.DecimalField(max_digits=5, decimal_places=2)
    sex = serializers.CharField()

class CompactUserSerializer(serializers.Serializer):
    username = serializers.CharField()

class BodypartSerializer(serializers.Serializer):
    name = serializers.CharField()

class ExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    is_unilateral = serializers.BooleanField()
    primary_bodyparts = BodypartSerializer(many=True)
    secondary_bodyparts = BodypartSerializer(many=True)
    created_by = CompactUserSerializer()
    shared_with = CompactUserSerializer(many=True)
    is_custom = serializers.SerializerMethodField()

    def get_is_custom(self, exercise):
        return exercise.is_custom()
    
class WorkoutSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()

class ExerciseSetSerializer(serializers.Serializer):
    workout = WorkoutSerializer()
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    reps = serializers.IntegerField()
    rir = serializers.IntegerField()
    wilksScore = serializers.DecimalField(max_digits=5, decimal_places=2)