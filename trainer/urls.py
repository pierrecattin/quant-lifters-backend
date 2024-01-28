from django.urls import path

from . import views

urlpatterns = [
    path("exercise/<exercise_name>/", views.getExercise, name="exercise"),
]