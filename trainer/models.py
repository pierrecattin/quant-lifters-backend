from django.db import models

class BodyPart(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=50, unique=True)

class Exercise(models.Model):
    def __str__(self):
        return self.name
    
    primary_bodyparts = models.ManyToManyField(BodyPart, related_name="primary_bodyparts", blank=True)
    secondary_bodyparts = models.ManyToManyField(BodyPart, related_name="secondary_bodyparts", blank=True)
    
    name = models.CharField(max_length=100, unique=True)
    fatigue_factor = models.IntegerField()

class User(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=200, unique=True)

class Workout(models.Model):
    def __str__(self):
        return "Workout at " + str(self.start_time)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField("Start time", auto_now=True)

class SetGroup(models.Model):
    def __str__(self):
        return "SetGroup in " + str(self.workout)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)

class Set(models.Model):
     def __str__(self):
        return str(self.exercise) + " " + str(self.reps) + "x" + str(self.weight) + "kg@RIR" + str(self.rir)
     setGroup = models.ForeignKey(SetGroup, on_delete=models.CASCADE)
     exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
     weight = models.DecimalField(decimal_places=1, max_digits=4)
     reps = models.IntegerField()
     rir = models.IntegerField(blank=True)

class IntensityTable(models.Model):
    def __str__(self):
        return str(self.exercise) + " instensity table for " + str(self.user)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise =  models.ForeignKey(Exercise, on_delete=models.CASCADE)
    percentages = models

class Intensity(models.Model):
    def __str__(self):
        return str(self.reps) + ": " + self.displayPercentage1RM()

    intensityTable = models.ForeignKey(IntensityTable, on_delete=models.CASCADE)
    reps = models.IntegerField()
    percentage1RM = models.DecimalField(decimal_places = 2, max_digits=4)
    
    def displayPercentage1RM(self):
        return str(round(100*self.percentage1RM,0))+"%"

