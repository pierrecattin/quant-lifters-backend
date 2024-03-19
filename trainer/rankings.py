from trainer.models import *
from django.db.models import Count, Sum, F, Func, FloatField

def ranking_query_set_to_json(query_set, ranking_label, query_set_headers, json_headers):
    data = [[q[q_header] for q_header in query_set_headers] for q in query_set]
    return {'label':ranking_label,'headers':json_headers,'data':data}

most_exercise_sets_query = (ExerciseSet.objects
        .select_related('workout')
        .select_related('workout__user')
        .values('workout__user__username')
        .annotate(number_sets=Count('workout__user__username'))
        .order_by('-number_sets')
    )

total_lifted_volume_query = (ExerciseSet.objects
        .select_related('workout')
        .select_related('workout__user')
        .values('workout__user__username')
        .annotate(volume=Sum(F('weight') * F('reps'), output_field=FloatField()))
        .order_by('-volume')
    )

def get_all_rankings():
    return [
        ranking_query_set_to_json(most_exercise_sets_query.all(), 'Most exercise sets', ['workout__user__username', 'number_sets'], ['User', 'Total number of sets']),
        ranking_query_set_to_json(total_lifted_volume_query.all(), 'Total lifted volume', ['workout__user__username', 'volume'], ['User', 'Total lifted volume'])
    ]