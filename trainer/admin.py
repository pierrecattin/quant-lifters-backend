from django.contrib import admin
from .models import *

class ExercisePrimaryBodypartInline(admin.TabularInline):
    model = ExercisePrimaryBodypart
    readonly_fields = ('id',)
    extra = 1

class ExerciseSecondaryBodypartInline(admin.TabularInline):
    model = ExerciseSecondaryBodypart
    readonly_fields = ('id',)
    extra = 1

class ExerciseSharedWith(admin.TabularInline):
    model = ExerciseSharedWith
    readonly_fields = ('id',)
    extra = 1

class ExerciseAdmin(admin.ModelAdmin):
    inlines = [ExercisePrimaryBodypartInline, ExerciseSecondaryBodypartInline, ExerciseSharedWith]

admin.site.register([ExerciseSet, Workout, Bodypart, Intensity, IntensityTable, User])
admin.site.register(Exercise, ExerciseAdmin)