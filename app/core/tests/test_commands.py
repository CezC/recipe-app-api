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
        patched_check.reaturn_value = True

        # we check if command was called if command is setup corectly
        call_command('wait_for_db')

        # check if check method was called

        # if was called with parameter (databse)
        patched_check.assert_called_once_with(database=['default'])
