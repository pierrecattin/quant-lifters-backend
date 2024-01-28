from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from trainer.models import Exercise

def getExercise(request, exercise_name:str):
    exercise = get_object_or_404(Exercise, pk=exercise_name)
    return HttpResponse(exercise.serialize())