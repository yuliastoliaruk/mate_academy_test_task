SELECT 
    DATE_TRUNC('week', leads.created_at) AS week_start,
    courses.type AS course_type,
    COUNT(leads.id) AS total_leads
FROM leads
JOIN courses ON leads.course_id = courses.id
GROUP BY week_start, course_type
ORDER BY week_start DESC, course_type;