from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("userisauthenticated", views.user_is_authenticated, name="userisauthenticated"),
    path("createuser", views.create_user, name="createuser"),
    path("userexerciseslog", views.user_exercises_log, name="userexercisedata"),
    path('workoutslog', views.workoutslog, name='workoutslog'),
    path("allbodyparts", views.all_bodyparts, name="allbodyparts"),
    path("saveexercisesets", views.save_exercise_sets, name= "saveexercisesets"),
    path("deleteexercisesets", views.delete_exercise_sets, name= "deleteexercisesets"),
    path("updateexercisesets", views.update_exercise_sets, name= "updateexercisesets"),
    path("createexercise", views.create_exercise, name="addexercise"),
    path("createexercisefamily", views.create_exercise_family, name="addexercisefamily"),
    path("createbodypart", views.create_bodypart, name="addbodypart"),
    path("userdetails", views.user_details, name="userdetails"),
    path("allrankings", views.all_rankings, name="allrankings"),
]