from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("userisauthenticated", views.UserIsAuthenticated, name="userisauthenticated"),
    path("createuser", views.CreateUser, name="createuser"),
    path("exercise/<exercise_name>/", views.GetExercise, name="exercise"),
    path("allexercises/", views.AllExercises, name="allexercises"),
    path("allbodyparts/", views.AllBodyparts, name="allbodyparts"),
    path("createexercise", views.CreateExercise, name="addexercise"),
    path("createbodypart", views.CreateBodypart, name="addbodypart"),
    path("userdetails", views.GetUserDetails, name="userdetails"),
]