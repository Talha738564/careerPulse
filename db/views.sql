CREATE OR REPLACE VIEW v_active_opportunities AS
SELECT o.* FROM opportunities o JOIN companies c ON c.company_id = o.company_id
WHERE o.status = 'ACTIVE' AND c.is_active = 'Y'
  AND (o.deadline IS NULL OR o.deadline >= TRUNC(SYSDATE));

CREATE OR REPLACE VIEW v_student_skill_profile AS
SELECT s.student_id, u.full_name, sk.skill_id, sk.skill_name, ss.proficiency, ss.years_experience
FROM students s JOIN users u ON u.user_id = s.user_id
JOIN student_skills ss ON ss.student_id = s.student_id
JOIN skills sk ON sk.skill_id = ss.skill_id;

CREATE OR REPLACE VIEW v_opportunity_skill_summary AS
SELECT o.opp_id, o.title,
  COUNT(CASE WHEN os.importance = 'REQUIRED' THEN 1 END) AS required_count,
  COUNT(CASE WHEN os.importance = 'PREFERRED' THEN 1 END) AS preferred_count
FROM opportunities o LEFT JOIN opportunity_skills os ON os.opp_id = o.opp_id
GROUP BY o.opp_id, o.title;

-- NULL = Not scored for roles with zero required skills. Preferred skills excluded.
CREATE OR REPLACE VIEW v_student_job_matches AS
SELECT s.student_id, o.opp_id,
  COUNT(os.skill_id) AS required_count, COUNT(ss.skill_id) AS matched_count,
  ROUND(100 * COUNT(ss.skill_id) / NULLIF(COUNT(os.skill_id), 0), 1) AS match_score
FROM students s CROSS JOIN v_active_opportunities o
LEFT JOIN opportunity_skills os ON os.opp_id = o.opp_id AND os.importance = 'REQUIRED'
LEFT JOIN student_skills ss ON ss.student_id = s.student_id AND ss.skill_id = os.skill_id
GROUP BY s.student_id, o.opp_id;
