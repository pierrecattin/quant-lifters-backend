from trainer.models import *
from django.db.models import Count, Sum, F, Func, FloatField

def ranking_query_set_to_json(query_set, ranking_label, score_label, user_header, score_header, details_label = None , details_header = None):
    users = [q[user_header] for q in query_set]
    scores = [q[score_header] for q in query_set]
    if details_label is None or details_header is None:
        return (
        {
            'label': ranking_label,
            'scoreLabel': score_label,
            'users': users,
            'scores': scores
        }
    )
    else:
        details = [q[details_header] for q in query_set]
        return (
            {
            'label': ranking_label,
            'scoreLabel': score_label,
            'users': users,
            'scores': scores,
            'details': details,
            'detailsLabel': details_label,
            }
        )

def get_all_rankings():
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
    
    def total_lifted_volume_query_to_json(query_set, ranking_label, score_label, user_header, score_header, details_label = None , details_header = None):
        users = [q[user_header] for q in query_set]
        scores = [round(q[score_header]/1000, 1) for q in query_set]
        if details_label is None or details_header is None:
            return (
            {
                'label': ranking_label,
                'scoreLabel': score_label,
                'users': users,
                'scores': scores
            }
    )
    
    return [
        ranking_query_set_to_json(most_exercise_sets_query.all(), 'Most Active Lifter', 'Total number of sets', 'workout__user__username', 'number_sets'),
        total_lifted_volume_query_to_json(total_lifted_volume_query.all(), 'King of Volume', 'Total lifted volume in tons', 'workout__user__username', 'volume')
    ]