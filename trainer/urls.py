from django.urls import path

from . import views

urlpatterns = [
    path('api-token-auth/', views.login),
    path("exercise/<exercise_name>/", views.GetExercise, name="exercise"),
    path("allexercises/", views.AllExercises, name="allexercises"),
    path("allbodyparts/", views.AllBodyparts, name="allbodyparts"),
    path("addexercise", views.AddExercise, name="addexercise"),
    path("addbodypart", views.AddBodypart, name="addbodypart"),
    path("userdetails", views.GetUserDetails, name="userdetails"),
    path("createuser", views.CreateUser, name="createuser"),
]