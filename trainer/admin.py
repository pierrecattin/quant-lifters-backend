from django.contrib import admin
from .models import *

class ExerciseFamilyPrimaryBodypartInline(admin.TabularInline):
    model = ExerciseFamilyPrimaryBodypart
    readonly_fields = ('id',)
    extra = 1

class ExerciseFamilySecondaryBodypartInline(admin.TabularInline):
    model = ExerciseFamilySecondaryBodypart
    readonly_fields = ('id',)
    extra = 1

class ExerciseSharedWithInline(admin.TabularInline):
    model = ExerciseSharedWith
    readonly_fields = ('id',)
    extra = 1

class ExerciseAdmin(admin.ModelAdmin):
    inlines = [ExerciseSharedWithInline]

class ExerciseFamilyAdmin(admin.ModelAdmin):
    inlines = [ExerciseFamilyPrimaryBodypartInline, ExerciseFamilySecondaryBodypartInline]

admin.site.register([ExerciseSet, Workout, Bodypart, Intensity, IntensityTable, User])
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ExerciseFamily, ExerciseFamilyAdmin)