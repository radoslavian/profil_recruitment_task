"""
Tests for the script.py.
"""
import os
import unittest
from unittest import mock
from unittest.mock import Mock, patch

import script


class EntryScriptTestCase(unittest.TestCase):
    def test_no_login(self):
        """
        Invoking the script with a task but without providing a login flag.
        """
        fail_status = 1
        wait_status = os.system("python ../script.py print-all-accounts "
                                "--password '6mKY!nP^+y'")
        exit_status = os.waitstatus_to_exitcode(wait_status)
        self.assertEqual(fail_status, exit_status)

    def test_no_password(self):
        """
        Invoking the script with a task but without providing
        a password flag.
        """
        fail_status = 1
        wait_status = os.system("python ../script.py print-all-accounts "
                                "--login 'abc@defg.hi'")
        exit_status = os.waitstatus_to_exitcode(wait_status)
        self.assertEqual(fail_status, exit_status)


class TasksTestCase(unittest.TestCase):
    def setUp(self):
        self.data_manager = Mock()
        self.data_manager.create_database = Mock()
        self.args = Mock()
        self.args.login = "login"
        self.args.password = "password"
        self.args.task = ""

    def _task(self):
        with mock.patch("script.DataManager") as DataManager:
            DataManager.return_value = self.data_manager
            try:
                script.main(self.args)
            except SystemExit:
                pass

        return DataManager

    def test_create_database(self):
        """
        Called with create_database command, the script should invoke
        DataManager constructor with the url of the database and
        instance.create_database with data directory path.
        No login or password are required.
        """
        self.args.login = ""
        self.args.password = ""
        self.args.task = "create_database"

        DataManager = self._task()
        DataManager.assert_called_with(script.DATABASE_URL)
        self.data_manager.create_database.assert_called_with(script.DATA_DIR)

    def test_log_in(self):
        """
        Logging-in to the DataManager.
        """
        self.args.task = "print-all-accounts"
        self._task()
        self.data_manager.log_in.assert_called_with(
            self.args.login, self.args.password)

    @mock.patch("builtins.print")
    def test_unrecognized_task(self, mock_print):
        """
        Providing flags but an unknown task.
        """
        self.args.task = "unknown_task"
        self._task()
        mock_print.assert_called_with("Unrecognized task.")

    @mock.patch("builtins.print")
    def test_print_all_accounts(self, mock_print):
        self.args.task = "print-all-accounts"
        self.data_manager.accounts_total_number = Mock()
        expected_return_value = "total number of accounts"
        self.data_manager.accounts_total_number\
            .return_value = expected_return_value
        self._task()

        self.data_manager.accounts_total_number.assert_called()
        mock_print.assert_called_with(expected_return_value)

    @mock.patch("script.print_oldest_account")
    def test_print_oldest_account(self, print_oldest_account):
        self.args.task = "print-oldest-account"
        self.data_manager.get_oldest_account = Mock()
        expected_return_value = "oldest account"
        self.data_manager.get_oldest_account\
            .return_value = expected_return_value
        self._task()

        self.data_manager.get_oldest_account.assert_called()
        print_oldest_account.assert_called_with(expected_return_value)

    @mock.patch("script.print_children_by_age")
    def test_group_by_age(self, group_children_by_age):
        self.args.task = "group-by-age"
        self.data_manager.group_children_by_age = Mock()
        expected_return_value = "children grouped by age"
        self.data_manager.group_children_by_age\
            .return_value = expected_return_value
        self._task()

        self.data_manager.group_children_by_age.assert_called()
        group_children_by_age.assert_called_with(expected_return_value)

    @mock.patch("script.print_children")
    def test_print_children(self, print_children):
        self.args.task = "print-children"
        self.data_manager.get_children = Mock()
        expected_return_value = "user's children"
        self.data_manager.get_children.return_value = expected_return_value
        self._task()

        self.data_manager.get_children.assert_called()
        print_children.assert_called_with(expected_return_value)

    @mock.patch("script.print_users_children_same_age")
    def test_find_similar_children_by_age(
            self, print_users_children_same_age):
        self.args.task = "find-similar-children-by-age"
        self.data_manager.users_w_similar_aged_children = Mock()
        expected_return_value = "found children of similar age"
        self.data_manager.users_w_similar_aged_children\
            .return_value = expected_return_value
        self._task()

        self.data_manager.users_w_similar_aged_children.assert_called()
        print_users_children_same_age.assert_called_with(
            expected_return_value)


if __name__ == '__main__':
    unittest.main()
