from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from json import dumps
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from trainer.auth import TokenAuthViaCookie
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from trainer.serializers import *
from trainer.models import Exercise, Bodypart, User


@api_view(['POST'])
@csrf_exempt  
def create_user(request):
    username = request.data.get('username') 
    email = request.data.get('email')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return HttpResponse(dumps({"error": "Username already taken"}), status=409)
    if User.objects.filter(email=email).exists():
        return HttpResponse(dumps({"error": "Email already used"}), status=409)
    user = User.objects.create_user(username, email, password)
    return HttpResponse(dumps(UserSerializer(user).data))

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse(dumps({"error": "Email not found"}), status=401)
    user = User.objects.get(email=email)
    if user.check_password(password):
        token, _ = Token.objects.get_or_create(user=user)
        response = HttpResponse()
        response["Set-Cookie"] =  "authToken="+token.key+"; SameSite=None; Secure; HttpOnly=true; Path=/; Max-Age=31536000"
        return response
    else:
        return HttpResponse(dumps({"error": 'Wrong password'}), status=401)
    
@api_view(['Get'])
def logout(request):
    response = HttpResponse()
    response["Set-Cookie"] =  "authToken=x; SameSite=None; Secure; HttpOnly=true; Path=/; Max-Age=31536000"
    return response
    
@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
def user_is_authenticated(request):
    response = {"is_authenticated": request.user.is_authenticated}
    return HttpResponse(dumps(response))

@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = User.objects.get(username=request.user)
    return HttpResponse(dumps(UserSerializer(user).data))

@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_exercises_log(request):
    user = request.user

    exercises = Exercise.objects.filter(
        models.Q(created_by__isnull=True) |
        models.Q(created_by=user) |
        models.Q(shared_with=user)
        ).distinct()

    exercises_data = []
    for exercise in exercises:
        exercise_data = ExerciseSerializer(exercise).data
        exercise_sets = ExerciseSet.objects.filter(exercise=exercise, workout__user=user)
        exercise_data['sets'] = ExerciseSetSerializer(exercise_sets, many=True).data
        exercises_data.append(exercise_data)

    return HttpResponse(dumps({"exercises":exercises_data}))

@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticated])
def all_bodyparts(request):
    bodyparts = Bodypart.objects.all()
    return HttpResponse(dumps({"bodyparts":[BodypartSerializer(b).data for b in bodyparts]}))

@api_view(['POST'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def save_exercise_sets(request):
    data = JSONParser().parse(request)
    exercise_sets_data = data["sets"]
    exercise_id = data["exercise_id"]
    time = data["time"]

    workout = Workout(user=request.user, start_time=time)
    workout.save()

    exercise = Exercise.objects.get(pk=exercise_id)
    for set_data in exercise_sets_data:
        exercise_set = ExerciseSet(workout=workout,
                                   exercise=exercise,
                                   reps=int(set_data["reps"]),
                                   weight=float(set_data["weight"]),
                                   rir=int(set_data["rir"]))
        exercise_set.save()
        
    return HttpResponse()


@api_view(['POST'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAdminUser])
@csrf_exempt
def create_exercise(request):
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
def create_bodypart(request):
    data = JSONParser().parse(request)
    bodypart = Bodypart(name=data['name'])
    bodypart.save()
    return HttpResponse(dumps(str(bodypart))) 
