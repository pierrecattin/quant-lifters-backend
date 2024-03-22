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
from trainer.models import *
from trainer.rankings import *


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
    # TODO: make more efficient
    user = request.user

    exercise_families = ExerciseFamily.objects.filter(
        models.Q(created_by__isnull=True) |
        models.Q(created_by=user) |
        models.Q(shared_with=user)
        )

    exercises = Exercise.objects.filter(
        models.Q(created_by__isnull=True) |
        models.Q(created_by=user) |
        models.Q(shared_with=user)
        )
    
    exercise_families_data = []
    for exercise_family in exercise_families:
        exercises = Exercise.objects.filter(
            models.Q(exercise_family=exercise_family) & (
            models.Q(created_by__isnull=True) |
            models.Q(created_by=user) |
            models.Q(shared_with=user))
        )
        exercises_data = []
        for exercise in exercises:
            exercise_data = ExerciseSerializer(exercise).data
            exercise_sets = ExerciseSet.objects.filter(exercise=exercise, workout__user=user)
            exercise_data["sets"] = ExerciseSetSerializerWithWorkout(exercise_sets, many=True).data
            exercises_data.append(exercise_data)
        exercise_familiy_data = ExerciseFamilySerializer(exercise_family).data
        exercise_familiy_data["exercises"] = exercises_data
        exercise_families_data.append(exercise_familiy_data)

    return HttpResponse(dumps({"exercise_families": exercise_families_data}))

@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticated])
def workoutslog(request):
    # TODO: make more efficient
    user = request.user
    workouts = Workout.objects.filter(user=user)
    workouts_data = []
    for workout in workouts:
        exercise_sets = ExerciseSet.objects.filter(workout=workout)
        if len(exercise_sets) > 0: 
            workout_data = WorkoutSerializer(workout).data
            workout_data['sets'] = ExerciseSetSerializerWithExercise(exercise_sets, many=True).data
            workouts_data.append(workout_data)
    return HttpResponse(dumps({"workouts": workouts_data}))

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

    workout = Workout(user=request.user, start_time=time, bodyweight=request.user.bodyweight)
    workout.save()

    exercise = Exercise.objects.get(pk=exercise_id)
    exercise_sets = []
    for set_data in exercise_sets_data:
        exercise_set = ExerciseSet(workout=workout,
                                   exercise=exercise,
                                   reps=int(set_data["reps"]),
                                   weight=float(set_data["weight"]),
                                   rir=int(set_data["rir"]))
        exercise_set.save()
        exercise_sets.append(exercise_set)
    response = [ExerciseSetSerializerWithWorkout(s).data for s in exercise_sets]
    return HttpResponse(dumps(response))

@api_view(['POST'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_exercise_sets(request):
    # TODO: prevent modifying sets of other users
    data = JSONParser().parse(request)
    exercise_sets_data = data["sets"]

    exercise_sets = []
    for set_data in exercise_sets_data:
        exercise_set = ExerciseSet.objects.get(pk=set_data["id"])
        exercise_set.reps = set_data["reps"]
        exercise_set.weight = set_data["weight"]
        exercise_set.rir = set_data["rir"]
        exercise_set.save()
        exercise_sets.append(exercise_set)
    response = [ExerciseSetSerializerWithWorkout(s).data for s in exercise_sets]
    return HttpResponse(dumps(response))

@api_view(['POST'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_exercise_sets(request):
    # TODO: prevent deleting sets of other users
    data = JSONParser().parse(request)
    set_ids = data["ids"]

    for set_id in set_ids:
        exercise_set = ExerciseSet.objects.get(pk=set_id)
        exercise_set.delete()
    return HttpResponse()


@api_view(['POST'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAdminUser])
@csrf_exempt
def create_exercise(request):
    data = JSONParser().parse(request)
    exercise = Exercise(name=data['name'], exercise_family=ExerciseFamily.objects.get(name=data['exercise_family']))
    exercise.save()
    return HttpResponse(dumps(ExerciseSerializer(exercise).data)) 
    
@api_view(['POST'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAdminUser])
@csrf_exempt
def create_bodypart(request):
    data = JSONParser().parse(request)
    bodypart = Bodypart(name=data['name'])
    bodypart.save()
    return HttpResponse(dumps(str(bodypart))) 

@api_view(['POST'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAdminUser])
@csrf_exempt
def create_exercise_family(request):
    data = JSONParser().parse(request)
    exercise_family = ExerciseFamily(name=data['name'])
    exercise_family.save()
    [exercise_family.primary_bodyparts.add(Bodypart.objects.get(name=b)) for b in data['primary_bodyparts']]
    [exercise_family.secondary_bodyparts.add(Bodypart.objects.get(name=b)) for b in data['secondary_bodyparts']]
    exercise_family.save()
    return HttpResponse(dumps(ExerciseFamilySerializer(exercise_family).data))

@api_view(['GET'])
@authentication_classes([TokenAuthViaCookie, BasicAuthentication])
@permission_classes([IsAuthenticated])
def all_rankings(request):
    return HttpResponse(dumps({"rankings":get_all_rankings()}))