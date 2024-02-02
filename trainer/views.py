from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from json import dumps
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view


from trainer.models import Exercise, Bodypart

@api_view(['GET'])
def GetExercise(request, exercise_name:str):
    exercise = get_object_or_404(Exercise, pk=exercise_name)
    return HttpResponse(dumps(exercise.serialize()))

@api_view(['GET'])
def AllExercises(request):
    exercises = Exercise.objects.all()
    return HttpResponse (dumps([e.serialize() for e in exercises]))

@api_view(['GET'])
def AllBodyparts(request):
    bodyparts = Bodypart.objects.all()
    return HttpResponse (dumps({"bodyparts":[str(b) for b in bodyparts]}))

@api_view(['POST'])
@csrf_exempt
def AddExercise(request):
    data = JSONParser().parse(request)
    exercise = Exercise(name=data['name'])
    exercise.save()
    return HttpResponse(dumps(exercise.serialize())) 
    