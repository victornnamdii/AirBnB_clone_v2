#!/usr/bin/python3
"""
Contains the unittests for console.py
"""

from io import StringIO
import console
import inspect
import pycodestyle
import sys
import unittest
from unittest.mock import patch
HBNBCommand = console.HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pep8_conformance_console(self):
        """Test that console.py conforms to Pycodestyle"""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")


class TestConsoleFunc(unittest.TestCase):
    """
    Testing the functionality of console.py
    """
    def test_help(self):
        """
        Testing the help method
        """
        out = "Shows an individual instance of a class\n"
        outa = "[Usage]: show <className> <objectId>\n\n"
        out2 = "Exits the program without formatting\n\n"
        out3 = "Exits the program with formatting\n\n"
        out4 = "*** No help on emptyline\n"
        out5 = "Creates a class of any type\n[Usage]: create <className>\n\n"
        out6 = "Destroys an individual instance of a class\n"
        outb = "[Usage]: destroy <className> <objectId>\n\n"
        out7 = "Shows all objects, or all of a class\n"
        outc = "[Usage]: all <className>\n\n"
        out8 = "Updates an object with new information\n"
        outd = "Usage: update <className> <id> <attName> <attVal>\n\n"
        out9 = "*** No help on default\n"

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            self.assertEqual(f.getvalue(), out + outa)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
            self.assertEqual(f.getvalue(), out2)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
            self.assertEqual(f.getvalue(), out3)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help emptyline")
            self.assertEqual(f.getvalue(), out4)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
            self.assertEqual(f.getvalue(), out5)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
            self.assertEqual(f.getvalue(), out6 + outb)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
            self.assertEqual(f.getvalue(), out7 + outc)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
            self.assertEqual(f.getvalue(), out8 + outd)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help default")
            self.assertEqual(f.getvalue(), out9)

    def test_create(self):
        """
        Testing create method
        """

        with patch('sys.stdout', new=StringIO()) as uuid:
            HBNBCommand().onecmd("create User")
            self.assertRegex(uuid.getvalue(),
                             '^[0-9a-f]{8}-[0-9a-f]{4}'
                             '-[0-9a-f]{4}-[0-9a-f]{4}'
                             '-[0-9a-f]{12}$')

        error = "** class name missing **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue(), error)

        error = "** class doesn't exist **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create duba")
            self.assertEqual(f.getvalue(), error)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="California"')
            self.assertRegex(f.getvalue(),
                             '^[0-9a-f]{8}-[0-9a-f]{4}'
                             '-[0-9a-f]{4}-[0-9a-f]{4}'
                             '-[0-9a-f]{12}$')
            HBNBCommand().onecmd("all State")
            self.assertTrue("California" in f.getvalue())

    def test_show(self):
        """
        Testing show method
        """

        error = "** class name missing **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual(f.getvalue(), error)

        error = "** class doesn't exist **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show duba")
            self.assertEqual(f.getvalue(), error)

        error = "** instance id missing **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual(f.getvalue(), error)

        error = "** no instance found **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show City sochi")
            self.assertEqual(f.getvalue(), error)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            uuid = f.getvalue()
            HBNBCommand().onecmd(f"show Amenity {uuid}")
            self.assertEqual(f.getvalue()[37:46], "[Amenity]")

    def test_destroy(self):
        """
        Testing destroy method
        """

        error = "** class name missing **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            self.assertEqual(f.getvalue(), error)

        error = "** class doesn't exist **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy duba")
            self.assertEqual(f.getvalue(), error)

        error = "** instance id missing **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Place")
            self.assertEqual(f.getvalue(), error)

        error = "** no instance found **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State sochi")
            self.assertEqual(f.getvalue(), error)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            uuid = f.getvalue()
            HBNBCommand().onecmd(f"destroy BaseModel {uuid}")
            HBNBCommand().onecmd(f"show BaseModel {uuid}")
            self.assertEqual(f.getvalue()[37:], error)

    def test_all(self):
        """
        Testing all method
        """

        error = "** class doesn't exist **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all duba")
            self.assertEqual(f.getvalue(), error)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            uuid = f.getvalue()
            HBNBCommand().onecmd("all State")
            hold = f.getvalue()[len(uuid):]
            self.assertFalse("User" in f.getvalue())
            HBNBCommand().onecmd("create BaseModel")
            uuid2 = f.getvalue()[len(uuid) + len(hold):]
            HBNBCommand().onecmd("all")
            hold2 = f.getvalue()[len(uuid) + len(hold) + len(uuid2):]
            self.assertTrue(len(hold2) > len(hold))
            self.assertTrue("BaseModel" in hold2)
            self.assertTrue("State" in hold2)

    def test_update(self):
        """
        Testing update method
        """

        error = "** class name missing **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            self.assertEqual(f.getvalue(), error)

        error = "** class doesn't exist **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update duba")
            self.assertEqual(f.getvalue(), error)

        error = "** instance id missing **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User")
            self.assertEqual(f.getvalue(), error)

        error = "** no instance found **\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update Review sochi")
            self.assertEqual(f.getvalue(), error)

        error = "** attribute name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            uuid = f.getvalue()
            HBNBCommand().onecmd(f"update User {uuid}")
            err = f.getvalue()[len(uuid):-1]
            self.assertEqual(err, error)

        error = "\n** value missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            uuid = f.getvalue()[:-1]
            HBNBCommand().onecmd(f"update User {uuid} first_name")
            err = f.getvalue()[len(uuid):-1]
            self.assertEqual(err, error)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            uuid = f.getvalue()[:-1]
            HBNBCommand().onecmd(f"update User {uuid} first_name sochi")
            HBNBCommand().onecmd(f"show User {uuid}")
            self.assertTrue(uuid in f.getvalue())
            self.assertTrue("User" in f.getvalue())
            self.assertTrue("first_name" in f.getvalue())
            self.assertTrue("sochi" in f.getvalue())

    # .all
    # .show
    # .destroy
    # .update
    # .count
