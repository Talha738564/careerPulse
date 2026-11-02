"""Optional Oracle query/transaction examples. Not enabled in the demo web app.
Live execution is pending a real Oracle instance; no connection at import time.
"""
from contextlib import contextmanager
import os
import oracledb
from dotenv import load_dotenv


def connect():
    load_dotenv()
    names = ('ORACLE_USER','ORACLE_PASSWORD','ORACLE_DSN')
    if not all(os.getenv(n) for n in names):
        raise RuntimeError('Configure ORACLE_USER, ORACLE_PASSWORD and ORACLE_DSN securely first.')
    return oracledb.connect(user=os.environ['ORACLE_USER'],password=os.environ['ORACLE_PASSWORD'],dsn=os.environ['ORACLE_DSN'])


@contextmanager
def transaction(connection):
    try:
        with connection.cursor() as cursor:
            yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise


def student_matches(connection, student_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT opp_id, required_count, matched_count, match_score FROM v_student_job_matches WHERE student_id=:student_id',
                       student_id=student_id)
        return [dict(zip(('opp_id','required_count','matched_count','match_score'),row)) for row in cursor]


def save_job(connection, student_id, opp_id):
    with transaction(connection) as cursor:
        cursor.execute('''MERGE INTO saved_jobs sj
            USING (SELECT :student_id AS student_id, :opp_id AS opp_id FROM dual) v
            ON (sj.student_id=v.student_id AND sj.opp_id=v.opp_id)
            WHEN NOT MATCHED THEN INSERT (student_id,opp_id) VALUES (v.student_id,v.opp_id)''',
            student_id=student_id,opp_id=opp_id)


def create_opportunity(connection, company_id, title, skill_ids):
    """Fictional role + required skills; a constraint failure rolls everything back."""
    with transaction(connection) as cursor:
        new_id=cursor.var(oracledb.NUMBER)
        cursor.execute('''INSERT INTO opportunities (company_id,title,job_type,is_demo,deadline)
            VALUES (:company_id,:title,'INTERNSHIP','Y',TRUNC(SYSDATE)+14)
            RETURNING opp_id INTO :new_id''',company_id=company_id,title=title,new_id=new_id)
        opp_id=int(new_id.getvalue()[0])
        for skill_id in set(skill_ids):
            cursor.execute("INSERT INTO opportunity_skills (opp_id,skill_id,importance) VALUES (:opp_id,:skill_id,'REQUIRED')",
                           opp_id=opp_id,skill_id=skill_id)
    return opp_id


if __name__ == '__main__':
    # Read-only readiness check; never installs schema or seed data automatically.
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1 FROM dual')
            assert cursor.fetchone()[0] == 1
        print('Oracle connection verified. Application integration still requires live tests.')
