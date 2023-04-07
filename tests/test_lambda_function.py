import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from src.lambda_function import lambda_handler

# Example test data
event = {"candle_time": "2023-04-05T18:45:00+03:00", "scheduled_for": 10}
context = Mock()

# Mock environment variables
@patch.dict('os.environ', {'BOT_TOKEN': 'test_token', 'BOT_CHATID': '["123", "456"]'})
def test_lambda_handler():
    # Mock the send_message function
    with patch('src.lambda_function.send_message') as mock_send_message:
        # Call the lambda_handler function
        lambda_handler(event, context)

        # Assert that send_message was called with the correct arguments
        mock_send_message.assert_called_once_with(
            f'Candle lighting time is in {event["scheduled_for"]} minutes at 18:45',
            ['123', '456']
        )
    with patch('src.lambda_function.get_chatids') as mock_get_chatids:
        # Call the lambda_handler function
        lambda_handler(event, context)

        # Assert that get_chatids was called with the correct arguments
        mock_get_chatids.assert_called_once_with()
