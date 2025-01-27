import unittest
from unittest.mock import patch, MagicMock
import os
with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///./test.db"}):
    from api.db.database import get_db

class TestGetDB(unittest.TestCase):

    @patch('api.db.database.SessionLocal')
    def test_get_db(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        
        db_gen = get_db()
        db = next(db_gen)
        
        self.assertEqual(db, mock_session)
        
        with self.assertRaises(StopIteration):
            next(db_gen)
        mock_session.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()