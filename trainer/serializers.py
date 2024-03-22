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

class ExerciseFamilySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    primary_bodyparts = BodypartSerializer(many=True)
    secondary_bodyparts = BodypartSerializer(many=True)
    created_by = CompactUserSerializer()
    shared_with = CompactUserSerializer(many=True)
    is_custom = serializers.SerializerMethodField()

    def get_is_custom(self, exercise_family):
        return exercise_family.is_custom()

class ExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    is_unilateral = serializers.BooleanField()
    created_by = CompactUserSerializer()
    shared_with = CompactUserSerializer(many=True)
    is_custom = serializers.SerializerMethodField()
    exercise_family = ExerciseFamilySerializer()

    def get_is_custom(self, exercise):
        return exercise.is_custom()

class CompactExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class WorkoutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    start_time = serializers.DateTimeField()

class ExerciseSetSerializerWithWorkout(serializers.Serializer):
    id = serializers.IntegerField()
    workout = WorkoutSerializer()
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    reps = serializers.IntegerField()
    rir = serializers.IntegerField()
    wilksScore = serializers.DecimalField(max_digits=5, decimal_places=2)

class ExerciseSetSerializerWithExercise(serializers.Serializer):
    id = serializers.IntegerField()
    exercise = CompactExerciseSerializer()
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    reps = serializers.IntegerField()
    rir = serializers.IntegerField()
    wilksScore = serializers.DecimalField(max_digits=5, decimal_places=2)