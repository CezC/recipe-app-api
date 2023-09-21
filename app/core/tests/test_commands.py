"""
Test custom Django management commands.
"""

# patch in order to mock behaviour of db
# to simulate responce from db
from unittest.mock import patch

# is posible error when we want to connect to db when it is not ready
from psycopg2 import OperationalError as Psycopg2Error

# helper function to call command by name to abel to run tested command
from django.core.management import call_command

# opteneital error exception depending on stage our startup process
from django.db.utils import OperationalError

# base test class used for testing.
# we use simple test case we test bechavior when db is not available
# we simulate behavior of db here
from django.test import SimpleTestCase

# mock behavior of our db
# path for differnt methods
# BaseCommand class parent class of our wait_for_db give.Command ass check method


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    # test if db is ready and we want to continue with execurion of our application
    def test_wait_for_db_ready(self, patched_check):
        """test wait for database if database ready"""
        # when we call check when it is called we reutrn True
        # here we mock object and return just simply True
        patched_check.reaturn_value = True

        # we check if command was called if command is setup corectly
        call_command('wait_for_db')

        # check if check method was called

        # if was called with parameter (databse)
        patched_check.assert_called_once_with(database=['default'])

    # test if db is not ready we should wait for it to be reade

    # test sleep method
    # we don't want to wait our unit test so we patch
    # replace sleep function wit magic mock it will return nonewalue
    # we owerwirte sleep to not wait.
    @patch('time.sleep')
    # in order first to last left to rignt arguments
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # we mock here object we raise exception like the db is not ready
        # we use side effect we pass different items and they will be handled
        # differently based on their tiype. we pass exception the mocking
        # library know to rise error
        # we pass boolean it will return boolean value
        # Firse two time * we call mock mecthod we want it to riese error
        # then we raise next 3 times OperationalError (because there are differnet
        # stages of postgres loading ) db not ready Psycopg2Error
        # next db is redy but test db is not ready so we rise OperationalErorr
        # then we return True.
        # he just chose 2 and 3 ties it seams as close to real situation can be more
        # next time we raturn True
        # \ is to put code in next line
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # we check if check is onlhy called 6 time 2 + 3 + 1
        # Psycopg2Error OperationalError and True
        self.assertEqual(patched_check.call_count, 6)
        # check if we run multiple check on our default db
        patched_check.assert_called_with(database=['default'])
