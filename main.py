import unittest
from app import get_doc_owner_name, add_new_doc, delete_doc
from unittest.mock import patch


class TestGetDocOwnerName(unittest.TestCase):
    def setUp(self):
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    @patch('builtins.input', return_value='10006')
    def test_get_doc_owner_name_10006(self, mock_input):
        self.assertEqual('Аристарх Павлов', get_doc_owner_name())

    @patch('builtins.input', return_value='')
    def test_get_doc_owner_name_none(self, mock_input):
        self.assertEqual(None, get_doc_owner_name())

    @unittest.expectedFailure
    @patch('builtins.input', return_value='10007')
    def test_get_doc_owner_name_10007(self, mock_input):
        self.assertEqual('Аристарх Павлов', get_doc_owner_name())


class TestAddNewDoc(unittest.TestCase):
    def setUp(self):
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    @patch('builtins.input', return_value='1111' and 'test' and 'Andrey' and '4')
    def test_add_new_doc_shelf_4(self, mock_input):
        self.assertEqual('4', add_new_doc())

    @patch('builtins.input', return_value='10006' and 'test' and 'Andrey' and '4')
    def test_add_new_doc_number_10006(self, mock_input):
        self.assertEqual('4', add_new_doc())


class TestDelDoc(unittest.TestCase):
    def setUp(self):
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    @patch('builtins.input', return_value='10006')
    def test_del_doc_number_10006(self, mock_input):
        self.assertEqual(('10006', True), delete_doc())

    @patch('builtins.input', return_value='')
    def test_del_doc_number_none(self, mock_input):
        self.assertEqual(None, delete_doc())

    @patch('builtins.input', return_value='10007')
    def test_del_doc_number_10007(self, mock_input):
        self.assertEqual(None, get_doc_owner_name())

    @unittest.expectedFailure
    @patch('builtins.input', return_value='11-2')
    def test_del_doc_number_11_2(self, mock_input):
        self.assertEqual('Василий Гупкин', get_doc_owner_name())


if __name__ == '__main__':
    unittest.main()
