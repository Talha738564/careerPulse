-- Demonstration for SQL Developer: declare the input bind variables first.
-- Insert an opportunity and its required skill as one transaction.
DECLARE
  new_opp_id NUMBER;
BEGIN
  SAVEPOINT before_opportunity;
  INSERT INTO opportunities (company_id,title,job_type,is_demo,deadline,status)
  VALUES (:company_id,:title,'INTERNSHIP','Y',TRUNC(SYSDATE)+14,'ACTIVE')
  RETURNING opp_id INTO new_opp_id;
  INSERT INTO opportunity_skills (opp_id,skill_id,importance)
  VALUES (new_opp_id,:skill_id,'REQUIRED');
  -- Caller decides COMMIT after reviewing both rows.
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK TO before_opportunity;
    RAISE;
END;
/
