import unittest
from unittest import mock

from src.codetrace_pse import cli

"""
I'm not actually confident with my mocking.
If I did it terribly, I will appreciate your comments.
"""


class TestScrape(unittest.TestCase):
    def setUp(self):
        self.symbol = 'BPI'

    def tearDown(self):
        pass

    # actually doing the function call
    def test_when_symbol_is_valid_not_mocked(self):
        return_keys = [
            'status', 'name', 'source_url',
            'curr_price', 'prev_price', 'open',
            'volume', 'high_52_week', 'low_52_week',
            'shares', 'sym'
        ]
        actual_return = cli.get_stock_details(self.symbol)
        self.assertEqual(return_keys, list(actual_return.keys()))
        self.assertEqual(self.symbol, actual_return['sym'])
        self.assertEqual('OK', actual_return['status'])

    # mocking the function call
    @mock.patch('src.codetrace_pse.cli.get_info')
    def test_when_symbol_is_valid_mocked(self, mock_get_info):
        expected_return = {
            'status': 'OK', 'sym': self.symbol
        }
        mock_get_info.return_value = expected_return
        actual_return = cli.get_stock_details(self.symbol)
        self.assertEqual(expected_return, actual_return)
        self.assertEqual(self.symbol, actual_return['sym'])
        self.assertEqual('OK', actual_return['status'])

    # mocking the function call
    @mock.patch('src.codetrace_pse.cli.get_info')
    def test_when_get_info_raised_exception_mocked(self, mock_get_info):
        ex = 'Test Ex'
        mock_obj = mock_get_info.return_value
        # mock_get_info.return_value = expected_return
        mock_obj.raiseError.side_effect = Exception(ex)
        actual_return = cli.get_stock_details(self.symbol)
        # print(actual_return)
        # self.assertEqual(expected_return, actual_return)
        self.assertRaises(Exception)


if __name__ == '__main__':
    unittest.main()
