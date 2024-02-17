from django.contrib.auth.models import AbstractUser
from django.db import models


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
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

#todo: add constraint that primary bodypart <> secondary bodypart
#todo: add constraint that you cannot share with yourself
#todo: "shared with" in admin dashboard adds an s: shared withs
   
class Exercise(models.Model):
    name = models.CharField(max_length=100)
    is_unilateral = models.BooleanField(default=False)
    primary_bodyparts = models.ManyToManyField(Bodypart, related_name="primary_bodyparts", through='ExercisePrimaryBodypart')
    secondary_bodyparts = models.ManyToManyField(Bodypart, related_name="secondary_bodyparts",  through='ExerciseSecondaryBodypart')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shared_with = models.ManyToManyField(User, related_name="shared_with", through='ExerciseSharedWith')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by'], name='unique_name_created_by_combination')
        ]

    def __str__(self):
        return self.name +("" if self.created_by is None else " created by " + str(self.created_by))

class ExercisePrimaryBodypart(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    primary_bodypart = models.ForeignKey(Bodypart, on_delete=models.CASCADE)

class ExerciseSecondaryBodypart(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    secondary_bodypart = models.ForeignKey(Bodypart, on_delete=models.CASCADE)

class ExerciseSharedWith(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)

class Workout(models.Model):
    lifter = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField("Start time", auto_now=True)
    
    def __str__(self):
        return str([str(exercise_set) for exercise_set in self.exerciseset_set.all()])

class ExerciseSet(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.DecimalField(decimal_places=1, max_digits=4)
    reps = models.IntegerField()
    rir = models.IntegerField(blank=True)
    def __str__(self):
        return str(self.exercise) + " " + str(self.reps) + "x" + str(self.weight) + "kg@RIR" + str(self.rir)


class IntensityTable(models.Model):
    lifter = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise =  models.ForeignKey(Exercise, on_delete=models.CASCADE)
    percentages = models
    
    def __str__(self):
        return str(self.exercise) + " instensity table for " + str(self.lifter) + ": " +  str(self.intensity_set.all())

class Intensity(models.Model):
    intensityTable = models.ForeignKey(IntensityTable, on_delete=models.CASCADE)
    reps = models.IntegerField()
    percentage1RM = models.DecimalField(decimal_places = 2, max_digits=4)

    def __str__(self):
        return str(self.reps) + ": " + self.displayPercentage1RM()
    
    def displayPercentage1RM(self):
        return str(round(100*self.percentage1RM,0))+"%"

