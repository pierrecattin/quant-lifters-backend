from django.contrib.auth.models import User
from django.db import models

class Bodypart(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name
    

class Exercise(models.Model):   
    name = models.CharField(max_length=100, primary_key=True)
    primary_bodyparts = models.ManyToManyField(Bodypart, related_name="primary_bodyparts", blank=True)
    secondary_bodyparts = models.ManyToManyField(Bodypart, related_name="secondary_bodyparts", blank=True)

    def __str__(self):
        return self.name
    
    def serialize(self):
        return {
            'name': self.name,
            'primary_bodyparts': [str(bp) for bp in self.primary_bodyparts.all()],
            'secondary_bodyparts':  [str(bp) for bp in self.secondary_bodyparts.all()],
            }

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise =  models.ForeignKey(Exercise, on_delete=models.CASCADE)
    percentages = models
    
    def __str__(self):
        return str(self.exercise) + " instensity table for " + str(self.user) + ": " +  str(self.intensity_set.all())

class Intensity(models.Model):
    intensityTable = models.ForeignKey(IntensityTable, on_delete=models.CASCADE)
    reps = models.IntegerField()
    percentage1RM = models.DecimalField(decimal_places = 2, max_digits=4)

    def __str__(self):
        return str(self.reps) + ": " + self.displayPercentage1RM()
    
    def displayPercentage1RM(self):
        return str(round(100*self.percentage1RM,0))+"%"

