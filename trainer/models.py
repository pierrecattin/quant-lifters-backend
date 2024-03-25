from django.contrib.auth.models import AbstractUser
from django.db import models

import numpy as np

class User(AbstractUser):

    bodyweight = models.FloatField(default=80.0)
    class Sex(models.TextChoices):
        MALE = 'male',
        FEMALE = 'female',
    
    sex = models.CharField(
        max_length=6,
        choices = Sex.choices,
        default = Sex.MALE,
    )



class Bodypart(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

   
class ExerciseFamily(models.Model):
    name = models.CharField(max_length=100)
    primary_bodyparts = models.ManyToManyField(Bodypart, related_name="primary_bodyparts", through='ExerciseFamilyPrimaryBodypart')
    secondary_bodyparts = models.ManyToManyField(Bodypart, related_name="secondary_bodyparts",  through='ExerciseFamilySecondaryBodypart')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shared_with = models.ManyToManyField(User, related_name="exercise_family_shared_with", through='ExerciseFamilySharedWith')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by'], name='unique_name_created_by_combination_exercise_family')
        ]

    def __str__(self):
        return self.name
    
    def is_custom(self):
        return self.created_by is not None

class ExerciseFamilySharedWith(models.Model):
    exercise_family = models.ForeignKey(ExerciseFamily, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)

class ExerciseFamilyPrimaryBodypart(models.Model):
    exercise_family = models.ForeignKey(ExerciseFamily, on_delete=models.CASCADE)
    primary_bodypart = models.ForeignKey(Bodypart, on_delete=models.CASCADE)


class ExerciseFamilySecondaryBodypart(models.Model):
    exercise_family = models.ForeignKey(ExerciseFamily, on_delete=models.CASCADE)
    secondary_bodypart = models.ForeignKey(Bodypart, on_delete=models.CASCADE)


#todo: add constraint that primary bodypart <> secondary bodypart
#todo: add constraint that you cannot share with yourself
#todo: "shared with" in admin dashboard adds an s: shared withs

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    is_unilateral = models.BooleanField(default=False)
    weight_factor = models.DecimalField(decimal_places=2, 
                                        max_digits=4, 
                                        default=1)
    bodyweight_inclusion_factor = models.DecimalField(decimal_places=2, 
                                                      max_digits=4, 
                                                      default=0)
    exercise_family = models.ForeignKey(ExerciseFamily, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shared_with = models.ManyToManyField(User, related_name="shared_with", through='ExerciseSharedWith')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by'], name='unique_name_created_by_combination'),
            models.CheckConstraint(check=models.Q(bodyweight_inclusion_factor__gte=0), name="bodyweight_inclusion_factor>=0"),
            models.CheckConstraint(check=models.Q(bodyweight_inclusion_factor__lte=1), name="bodyweight_inclusion_factor<=0"),
            models.CheckConstraint(check=models.Q(weight_factor__gte=0), name="weight_factor>=0"),
        ]

    def __str__(self):
        return self.name +("" if self.created_by is None else " created by " + str(self.created_by))
    
    def is_custom(self):
        return self.created_by is not None


class ExerciseSharedWith(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField("Start time", auto_now=True)
    bodyweight = models.FloatField(default=80.0)
    
    def __str__(self):
        return str([str(exercise_set) for exercise_set in self.exerciseset_set.all()])

class ExerciseSet(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.DecimalField(decimal_places=2, max_digits=6)
    reps = models.IntegerField()
    rir = models.IntegerField(blank=True)
    
    @property
    def wilksScore(self):
        if self.workout.user.sex == 'female':
            wilksFormulaConstants = np.array([594.31747775582, -27.23842536447, 0.82112226871, -0.00930733913, 0.00004731582, -0.00000009054])
        else:
            wilksFormulaConstants = np.array([-216.0475144, 16.2606339, -0.002388645, -0.00113732, 0.00000701863, -0.00000001291])
        powersOfBodyweight = np.array([pow(self.workout.user.bodyweight, power) for power in range(6)])
        wilksCoefficient = 500 / np.dot(powersOfBodyweight, wilksFormulaConstants)
        return float(self.weight) * wilksCoefficient
    
    def __str__(self):
        return str(self.exercise) + " " + str(self.reps) + "x" + str(self.weight) + "kg@RIR" + str(self.rir)


class IntensityTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise =  models.ForeignKey(Exercise, on_delete=models.CASCADE)
    percentages = models
    
    def __str__(self):
        return str(self.exercise) + " intensity table for " + str(self.user) + ": " +  str(self.intensity_set.all())

class Intensity(models.Model):
    intensityTable = models.ForeignKey(IntensityTable, on_delete=models.CASCADE)
    reps = models.IntegerField()
    percentage1RM = models.DecimalField(decimal_places = 2, max_digits=4)

    def __str__(self):
        return str(self.reps) + ": " + self.displayPercentage1RM()
    
    def displayPercentage1RM(self):
        return str(round(100*self.percentage1RM,0))+"%"

