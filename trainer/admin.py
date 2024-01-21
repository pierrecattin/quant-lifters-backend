from django.contrib import admin

from .models import *

admin.site.register([Exercise, Set, Workout, BodyPart, User, SetGroup, Intensity, IntensityTable])