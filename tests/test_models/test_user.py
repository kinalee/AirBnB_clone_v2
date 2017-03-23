import unittest
from datetime import datetime
import os
if os.getenv('HBNB_TYPE_STORAGE') == "db":
    os.putenv('HBNB_TYPE_STORAGE', "kappa")
from models import User


class Test_UserModel(unittest.TestCase):
    """
    Test the user model class
    """

    def setUp(self):
        self.model = User()

    def test_var_initialization(self):
        self.assertTrue(hasattr(self.model, "email"))
        self.assertTrue(hasattr(self.model, "password"))
        self.assertTrue(hasattr(self.model, "first_name"))
        self.assertTrue(hasattr(self.model, "last_name"))
        """self.assertEqual(self.model.email, "")
        self.assertEqual(self.model.password, "")
        self.assertEqual(self.model.first_name, "")
        self.assertEqual(self.model.last_name, "")"""


if __name__ == "__main__":
    unittest.main()
