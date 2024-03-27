WITH 
	es_enriched AS (
		SELECT 
			es_tw.*,		
			es_tw.total_weight * es_tw.reps AS volume,
			es_tw.total_weight * (1 + 0.033 * (es_tw.reps + es_tw.rir - 1)) AS one_rep_max
		FROM (
			SELECT 
				es.*,
				es.weight + e.bodyweight_inclusion_factor * w.bodyweight AS total_weight,
				u.username AS username,
				e.name AS exercise_name,
				w.start_time As start_time
			FROM trainer_exerciseset es
			LEFT JOIN trainer_exercise e ON es.exercise_id = e.id
			LEFT JOIN trainer_workout w ON es.workout_id = w.id
			LEFT JOIN trainer_user u ON w.user_id =u.id
		) es_tw
	),
	stats AS (
		SELECT 
			es_enriched.username, 
			es_enriched.exercise_id, 
			es_enriched.exercise_name,
			sum(es_enriched.reps) as number_reps,
			sum(es_enriched.volume) as total_volume,
			count(*) as number_sets,
			max(es_enriched.one_rep_max) as one_rep_max,
			max(es_enriched.total_weight) as max_weight
		FROM es_enriched
		GROUP BY es_enriched.username, es_enriched.exercise_id, es_enriched.exercise_name
	),
	orm_details AS (
		SELECT 
			es_enriched.exercise_id AS exercise_id,
			es_enriched.username AS username,
			MAX(
				CONCAT(
					CAST(DATE(es_enriched.start_time) AS varchar), '/',
				    RIGHT(CONCAT('00', CAST(es_enriched.weight AS varchar)), 6), '/',
					RIGHT(CONCAT('0', CAST(es_enriched.reps AS varchar)), 2), '/',
					RIGHT(CONCAT('0', CAST(es_enriched.rir AS varchar)), 2)
					)
			) AS set_details
		FROM es_enriched
		RIGHT JOIN stats
		ON es_enriched.username = stats.username AND
			es_enriched.exercise_id = stats.exercise_id AND
			es_enriched.one_rep_max = stats.one_rep_max
		GROUP BY 
			es_enriched.exercise_id, es_enriched.username
	),
	mw_details AS (
		SELECT 
			es_enriched.exercise_id AS exercise_id,
			es_enriched.username AS username,
			MAX(
				CONCAT(
					CAST(DATE(es_enriched.start_time) AS varchar), '/',
				    RIGHT(CONCAT('00', CAST(es_enriched.weight AS varchar)), 6), '/',
					RIGHT(CONCAT('0', CAST(es_enriched.reps AS varchar)), 2), '/',
					RIGHT(CONCAT('0', CAST(es_enriched.rir AS varchar)), 2)
				)
			) AS set_details
		FROM es_enriched
		RIGHT JOIN stats
			ON es_enriched.username = stats.username AND
				es_enriched.exercise_id = stats.exercise_id AND
				es_enriched.total_weight = stats.max_weight
		GROUP BY 
			es_enriched.exercise_id, es_enriched.username
	)
SELECT 
	stats.*, orm_details.set_details AS one_rep_max_details,
	mw_details.set_details AS max_weight_details
FROM stats
LEFT JOIN orm_details
	ON orm_details.username = stats.username AND
		orm_details.exercise_id = stats.exercise_id
LEFT JOIN mw_details
	ON mw_details.username = stats.username AND
		mw_details.exercise_id = stats.exercise_id
