import unittest
import sys
import io
from contextlib import contextmanager
from models import *
from datetime import datetime
from console import HBNBCommand
from models.engine.file_storage import FileStorage


@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class Test_Console(unittest.TestCase):
    """
    Test the console
    """

    @classmethod
    def setUpClass(cls):
        cls.cli = HBNBCommand()
        cls.cli.storage._FileStorage__objects = {}
        cls.cli.storage._FileStorage__file_path = "atestfile.json"

    def setUp(self):
        self.test_args = {'TESTINGITEM': "THIS IS A TESTING ITEM",
                          'integeritem': 11,
                          'floatitem': 1.1111111111}
        self.test_objects = []
        for valid_class in self.cli.valid_classes:
            obj = eval(valid_class)(**self.test_args)
            self.test_objects.append((valid_class, obj.id, obj))
            self.cli.storage.new(obj)
        self.cli.storage.save()

    def tearDown(self):
        import os
        if os.path.isfile(self.cli.storage._FileStorage__file_path):
            os.remove(self.cli.storage._FileStorage__file_path)

    def test_quit(self):
        with self.assertRaises(SystemExit):
            self.cli.do_quit(self.cli)

    def test_show(self):
        for item in self.test_objects:
            with captured_output() as (out, err):
                self.cli.do_show("{} {}".format(item[0], item[1]))
            output = out.getvalue().strip()
            self.assertIn(item[0], output)
            self.assertIn(item[1], output)
            self.assertIn(str(item[2]), output)

    def test_all(self):
        with captured_output() as (out, err):
            self.cli.do_all()
        output = out.getvalue().strip()
        for obj in self.test_objects:
            self.assertIn(obj[1], output)

    def test_all_with_class(self):
        for item in self.cli.valid_classes:
            with captured_output() as (out, err):
                self.cli.do_all(item)
            output = out.getvalue().strip()
            self.assertIn(item, output)
            for other_class in self.cli.valid_classes:
                if other_class is not item:
                    self.assertNotIn("[{} (".format(other_class), output)

    def test_all_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_all("Human")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_show_error_no_args(self):
        with captured_output() as (out, err):
            self.cli.do_show('')
        output = out.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    def test_show_error_missing_arg(self):
        with captured_output() as (out, err):
            self.cli.do_show("BaseModel")
        output = out.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

    def test_show_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_show("Human 1234-5678-9101")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_show_error_class_missing(self):
        with captured_output() as (out, err):
            self.cli.do_show("d3da85f2-499c-43cb-b33d-3d7935bc808c")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_create_empty(self):
        with captured_output() as (out, err):
            self.cli.do_create('')
        output = out.getvalue().strip()
        expected = ", ".join(self.cli.valid_classes)
        expected = "Usage: create [{:s}]".format(expected)
        self.assertEqual(output, expected)

    def test_create_noargs(self):
        with captured_output() as (out, err):
            self.cli.do_create("BaseModel")
        output = out.getvalue().strip()
        with captured_output() as (out, err):
            self.cli.do_show("BaseModel {}".format(output))
        output2 = out.getvalue().strip()
        self.assertIn(output, output2)

    def test_destroy_created(self):
        for item in self.test_objects:
            with captured_output() as (out, err):
                self.cli.do_show("{} {}".format(item[0], item[1]))
            output = out.getvalue().strip()
            self.assertEqual(output, str(item[2]))

            self.cli.do_destroy("{} {}".format(item[0], item[1]))
            with captured_output() as (out, err):
                self.cli.do_show("{} {}".format(item[0], item[1]))
            output = out.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_destroy_error_missing_id(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("BaseModel")
        output = out.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

    def test_destroy_error_class_missing(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("d3da85f2-499c-43cb-b33d-3d7935bc808c")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_destroy_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("Human d3da85f2-499c-43cb-b33d-3d7935bc808c")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_destroy_error_invalid_id(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("BaseModel " +
                                "f519fb40-1f5c-458b-945c-2ee8eaaf4900")
        output = out.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_update_correct(self):
        for item in self.test_objects:
            with captured_output() as (out, err):
                self.cli.do_update("{} {} TESTINGNAME PHILIPYOO".format(
                                   item[0], item[1]))
            output = out.getvalue().strip()
            self.assertEqual(output, "")

            with captured_output() as (out, err):
                self.cli.do_show("{} {}".format(item[0], item[1]))
            output = out.getvalue().strip()
            self.assertIn("TESTINGNAME", output)
            self.assertIn("PHILIPYOO", output)

    def test_update_error_invalid_id(self):
        with captured_output() as (out, err):
            self.cli.do_update("BaseModel ffffffff-edcb-a111-000000000000 name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_update_error_no_id(self):
        with captured_output() as (out, err):
            self.cli.do_update("BaseModel name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** value missing **")

    def test_update_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_update("Human " +
                               "d3da85f2-499c-43cb-b33d-3d7935bc808c name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update_error_no_class(self):
        with captured_output() as (out, err):
            self.cli.do_update("d3da85f2-499c-43cb-b33d-3d7935bc808c name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update_error_missing_value(self):
        with captured_output() as (out, err):
            self.cli.do_update("BaseModel " +
                               "d3da85f2-499c-43cb-b33d-3d7935bc808c name")
        output = out.getvalue().strip()
        self.assertEqual(output, "** value missing **")

if __name__ == "__main__":
    unittest.main()
