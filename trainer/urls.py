from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("userisauthenticated", views.user_is_authenticated, name="userisauthenticated"),
    path("createuser", views.create_user, name="createuser"),
    path("userexerciseslog", views.user_exercises_log, name="userexercisedata"),
    path("allbodyparts", views.all_bodyparts, name="allbodyparts"),
    path("createexercise", views.create_exercise, name="addexercise"),
    path("createbodypart", views.create_bodypart, name="addbodypart"),
    path("userdetails", views.user_details, name="userdetails"),
]