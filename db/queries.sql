-- Bind :student_id, :query, :city and :job_type in your Oracle client/driver.
-- Joins + parameterized discovery. '%' means list all when query is NULL.
SELECT o.opp_id, o.title, c.company_name, m.match_score
FROM v_active_opportunities o JOIN companies c ON c.company_id=o.company_id
JOIN v_student_job_matches m ON m.opp_id=o.opp_id AND m.student_id=:student_id
WHERE (:city IS NULL OR LOWER(o.city)=LOWER(:city))
  AND (:job_type IS NULL OR o.job_type=:job_type)
  AND (LOWER(o.title) LIKE '%' || LOWER(:query) || '%'
       OR LOWER(c.company_name) LIKE '%' || LOWER(:query) || '%')
ORDER BY m.match_score DESC NULLS LAST;

-- Missing required skills (correlated NOT EXISTS).
SELECT o.opp_id, sk.skill_name FROM v_active_opportunities o
JOIN opportunity_skills os ON os.opp_id=o.opp_id AND os.importance='REQUIRED'
JOIN skills sk ON sk.skill_id=os.skill_id
WHERE NOT EXISTS (SELECT 1 FROM student_skills ss
                  WHERE ss.student_id=:student_id AND ss.skill_id=os.skill_id);

-- Skill demand: denominator includes active jobs with no requirements.
SELECT sk.skill_name, COUNT(DISTINCT os.opp_id) AS jobs_requiring_skill,
 ROUND(100 * COUNT(DISTINCT os.opp_id) /
       NULLIF((SELECT COUNT(*) FROM v_active_opportunities),0),1) AS demand_percent
FROM skills sk JOIN opportunity_skills os ON os.skill_id=sk.skill_id
JOIN v_active_opportunities o ON o.opp_id=os.opp_id
WHERE os.importance='REQUIRED' GROUP BY sk.skill_name
ORDER BY jobs_requiring_skill DESC;

-- Companies with their job counts, including companies with zero jobs.
SELECT c.company_name, COUNT(o.opp_id) AS job_count
FROM companies c LEFT JOIN opportunities o ON o.company_id=c.company_id
GROUP BY c.company_id,c.company_name;

-- Aggregation and scalar subquery.
SELECT job_type, AVG(min_salary) AS average_minimum FROM v_active_opportunities GROUP BY job_type;
SELECT opp_id,title,min_salary FROM v_active_opportunities
WHERE min_salary > (SELECT AVG(min_salary) FROM v_active_opportunities);

-- Deadline Pulse; inspect before notification generation.
SELECT sj.student_id,o.opp_id,o.title,o.deadline
FROM saved_jobs sj JOIN v_active_opportunities o ON o.opp_id=sj.opp_id
WHERE o.deadline BETWEEN TRUNC(SYSDATE) AND TRUNC(SYSDATE)+7;

-- Student-interest analytics. Clicks do not imply submitted applications.
SELECT o.opp_id,o.title,COUNT(sj.saved_id) AS saved_count
FROM opportunities o LEFT JOIN saved_jobs sj ON sj.opp_id=o.opp_id
GROUP BY o.opp_id,o.title ORDER BY saved_count DESC;
SELECT opp_id,COUNT(*) AS click_count FROM apply_clicks GROUP BY opp_id;

-- Idempotent new-match generation (any selected skill + all other criteria).
MERGE INTO notifications n
USING (
 SELECT s.user_id,o.opp_id,a.alert_name,
        'match:' || a.alert_id || ':' || o.opp_id AS event_key
 FROM job_alerts a JOIN students s ON s.student_id=a.student_id
 CROSS JOIN v_active_opportunities o
 WHERE a.is_active='Y'
   AND (a.city IS NULL OR LOWER(a.city)=LOWER(o.city))
   AND (a.job_type IS NULL OR a.job_type=o.job_type)
   AND (a.is_remote_only='N' OR o.is_remote='Y')
   AND (a.min_salary IS NULL OR o.min_salary>=a.min_salary)
   AND (NOT EXISTS (SELECT 1 FROM job_alert_skills jas WHERE jas.alert_id=a.alert_id)
        OR EXISTS (SELECT 1 FROM job_alert_skills jas JOIN opportunity_skills os
                   ON os.skill_id=jas.skill_id AND os.importance='REQUIRED'
                   WHERE jas.alert_id=a.alert_id AND os.opp_id=o.opp_id))
) m ON (n.user_id=m.user_id AND n.event_key=m.event_key)
WHEN NOT MATCHED THEN INSERT
 (user_id,opp_id,title,message,notification_type,event_key)
 VALUES (m.user_id,m.opp_id,'New match','A role matches ' || m.alert_name,'NEW_MATCH',m.event_key);
-- Review before COMMIT; ROLLBACK discards notification inserts in this transaction.
