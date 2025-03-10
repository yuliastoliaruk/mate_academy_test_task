SELECT 
	domains.slug, 
	COUNT(leads.id) AS won_leads_count
FROM leads
JOIN users ON leads.user_id = users.id
JOIN domains ON users.domain_id = domains.id
WHERE leads.status = 'WON' 
	AND leads.created_at > '2024-01-01'::TIMESTAMPTZ
GROUP BY domains.slug;