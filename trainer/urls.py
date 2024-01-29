from django.urls import path

from . import views

urlpatterns = [
    path("exercise/<exercise_name>/", views.GetExercise, name="exercise"),
    path("allexercises/", views.AllExercisesNames, name="allexercises"),
    path("addexercise", views.AddExercise, name="addexercise"),
]