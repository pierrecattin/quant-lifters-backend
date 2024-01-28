from django.contrib import admin

from .models import *

admin.site.register([Exercise, ExerciseSet, Workout, BodyPart, User, Intensity, IntensityTable])