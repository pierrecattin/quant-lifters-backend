import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth('username', 'password')

backend_url = ['http://localhost:8000/trainer/', 'https://quant-lifters.onrender.com/trainer/'][0]

file = "./DevTools/initial_data.xlsx"
bodyparts = pd.read_excel(file, sheet_name="bodyparts", header=0)
exercises = pd.read_excel(file, sheet_name="exercises", header=0)
exercise_families = pd.read_excel(file, sheet_name="exercise_families", header=0)
exercise_families = exercise_families.fillna('')

for bodypart in bodyparts.name:
    payload = {'name': bodypart}
    print(bodypart)

    x=requests.post(backend_url+"createbodypart", json = payload, auth=auth)


def saveExerciseFamily(exercise_family):
    print(exercise_family.title)
    payload = {'name': exercise_family.title,
               'primary_bodyparts': exercise_family.primary_bodyparts.split(','),
               'secondary_bodyparts': exercise_family.secondary_bodyparts.split(',')}

    x=requests.post(backend_url+"createexercisefamily", json = payload, auth=auth)

exercise_families.apply(saveExerciseFamily, axis=1)


def saveExercise(exercise):
    print(exercise.title)
    payload = {'name': exercise.title,
               'exercise_family': exercise.exercise_family}

    x=requests.post(backend_url+"createexercise", json = payload, auth=auth)

exercises.apply(saveExercise, axis=1)