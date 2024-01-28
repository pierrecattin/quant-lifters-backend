from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from json import dumps
from trainer.models import Exercise

def GetExercise(request, exercise_name:str):
    exercise = get_object_or_404(Exercise, pk=exercise_name)
    return HttpResponse(dumps(exercise.serialize()))

def AllExercisesNames(request):
    exercises = Exercise.objects.all()
    return HttpResponse (dumps([e.serialize() for e in exercises]))