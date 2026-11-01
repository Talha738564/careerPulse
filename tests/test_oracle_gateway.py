import unittest
from unittest.mock import MagicMock
from db.oracle_gateway import transaction, save_job, student_matches

class OracleGatewayTests(unittest.TestCase):
    def connection(self):
        connection=MagicMock()
        return connection,connection.cursor.return_value.__enter__.return_value

    def test_success_commits_and_error_rolls_back(self):
        connection,cursor=self.connection()
        with transaction(connection):
            pass
        connection.commit.assert_called_once()
        connection.rollback.assert_not_called()
        connection,cursor=self.connection()
        with self.assertRaises(RuntimeError):
            with transaction(connection):
                raise RuntimeError('constraint failure')
        connection.rollback.assert_called_once()
        connection.commit.assert_not_called()

    def test_save_uses_bound_values_and_transaction(self):
        connection,cursor=self.connection()
        save_job(connection,7,13)
        sql=cursor.execute.call_args.args[0]
        self.assertIn(':student_id',sql)
        self.assertIn(':opp_id',sql)
        self.assertEqual(cursor.execute.call_args.kwargs,dict(student_id=7,opp_id=13))
        connection.commit.assert_called_once()
        cursor.execute.side_effect=RuntimeError('failed write')
        with self.assertRaises(RuntimeError):
            save_job(connection,7,13)
        connection.rollback.assert_called_once()

    def test_match_mapping_preserves_null_score(self):
        connection,cursor=self.connection()
        cursor.__iter__.return_value=iter([(2,0,0,None),(3,3,2,66.7)])
        rows=student_matches(connection,8)
        self.assertIsNone(rows[0]['match_score'])
        self.assertEqual(rows[1]['match_score'],66.7)
        self.assertEqual(cursor.execute.call_args.kwargs,dict(student_id=8))
