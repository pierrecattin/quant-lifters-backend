from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from json import dumps
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from trainer.auth import TokenAuthViaCookie
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from trainer.serializers import UserSerializer
from trainer.models import Exercise, Bodypart, User


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        response = HttpResponse()
        response["Set-Cookie"] =  'authToken='+token.key+"; SameSite=None; Secure; HttpOnly=true; Path=/; Max-Age=31536000"
        return response
    else:
        return HttpResponse('Invalid login', status=401)
    
@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
def UserIsAuthenticated(request):
    response = {"is_authenticated": request.user.is_authenticated}
    return HttpResponse(dumps(response))

@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticated])
def GetUserDetails(request):
    user = User.objects.get(username=request.user)
    return HttpResponse(dumps(UserSerializer(user).data))

@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticated])
def GetExercise(request, exercise_name:str):
    exercise = get_object_or_404(Exercise, pk=exercise_name)
    return HttpResponse(dumps(exercise.serialize()))

@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticated])
def AllExercises(request):
    exercises = Exercise.objects.all()
    return HttpResponse(dumps([e.serialize() for e in exercises]))

@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticated])
def AllBodyparts(request):
    bodyparts = Bodypart.objects.all()
    return HttpResponse(dumps({"bodyparts":[str(b) for b in bodyparts]}))

@api_view(['POST'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAdminUser])
@csrf_exempt
def CreateExercise(request):
    data = JSONParser().parse(request)
    exercise = Exercise(name=data['name'])
    exercise.save()
    [exercise.primary_bodyparts.add(Bodypart.objects.get(pk=b)) for b in data['primary_bodyparts']]
    [exercise.secondary_bodyparts.add(Bodypart.objects.get(pk=b)) for b in data['secondary_bodyparts']]
    exercise.save()
    return HttpResponse(dumps(exercise.serialize())) 
    
@api_view(['POST'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAdminUser])
@csrf_exempt
def CreateBodypart(request):
    data = JSONParser().parse(request)
    bodypart = Bodypart(name=data['name'])
    bodypart.save()
    return HttpResponse(dumps(str(bodypart))) 

@api_view(['POST'])
@csrf_exempt  
def CreateUser(request):
    data = JSONParser().parse(request)
    user = User.objects.create_user(data["username"], data["email"], data["password"])
    return HttpResponse(dumps(UserSerializer(user).data))