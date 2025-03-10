SELECT 
	users.email, 
	leads.id,
	leads.lost_reason
FROM leads
JOIN users ON leads.user_id = users.id
JOIN courses ON leads.course_id = courses.id
WHERE leads.status = 'LOST'
	AND courses.type = 'FLEX'
	AND leads.updated_at >= '2024-07-01'::TIMESTAMPTZ;