import unittest
import os.path
from datetime import datetime
from models.engine.file_storage import FileStorage
from models import *
from console import HBNBCommand


class Test_DBStorage(unittest.TestCase):
    """
    Tests the DBStorage class
    """

    @classmethod
    def setUpClass(cls):
        cls.storage = FileStorage()
        cls.storage._FileStorage__objects = {}
        cls.storage._FileStorage__file_path = "atestfile.json"

    def setUp(self):
        self.test_args = {'TESTINGITEM': "THIS IS A TESTING ITEM",
                          'integeritem': 11,
                          'floatitem': 1.11111111}
        self.test_objects = []
        for valid_class in HBNBCommand.valid_classes:
            obj = eval(valid_class)(**self.test_args)
            self.test_objects.append((valid_class, obj.id, obj))
        self.storage._FileStorage__objects = {}

    def tearDown(self):
        try:
            os.remove("atestfile.json")
        except:
            pass

    def test_all(self):
        self.assertEqual(self.storage._FileStorage__objects,
                         self.storage.all())

    def test_new(self):
        for item in self.test_objects:
            self.storage.new(item[2])
        self.assertEqual(len(self.storage.all()),
                         len(self.test_objects))

    def test_save(self):
        for item in self.test_objects:
            self.storage.new(item[2])
        self.storage.save()
        new_storage = FileStorage()
        new_storage._FileStorage__objects = {}
        new_storage._FileStorage__file_path = "atestfile.json"
        new_storage.reload()
        for key in self.storage.all():
            self.assertIn(key, new_storage.all())

    def test_reload(self):
        self.test_save()

if __name__ == "__main__":
    unittest.main()
