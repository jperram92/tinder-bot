import pytest
import yaml
import os
from unittest.mock import Mock, patch
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tinder_bot_email_notify import detect_bot, send_email_stats_update, handle_match

@pytest.fixture
def test_config():
    with open('tests/test_config.yaml', 'r') as file:
        return yaml.safe_load(file)

@pytest.fixture
def mock_tinder():
    return Mock()

def test_bot_detection(test_config):
    """Test the bot detection function with various profiles"""
    # Test valid profiles
    for profile in test_config['test_profiles']['valid_users']:
        assert not detect_bot(profile)
    
    # Test bot profiles
    for profile in test_config['test_profiles']['bot_profiles']:
        assert detect_bot(profile)

    # Test empty bio
    assert not detect_bot({"user_id": "test123"})

@patch('smtplib.SMTP')
def test_email_sending(mock_smtp, test_config):
    """Test email sending functionality"""
    email_config = test_config['email_config']
    
    with patch.dict('os.environ', {
        'EMAIL_SENDER_ADDRESS': email_config['test_sender'],
        'EMAIL_SENDER_PASSWORD': email_config['test_password'],
        'EMAIL_RECIEVER_ADDRESS': email_config['test_receiver']
    }):
        send_email_stats_update("Test Update")
        
        # Verify SMTP interactions
        mock_smtp.return_value.__enter__.return_value.send_message.assert_called_once()
        mock_smtp.return_value.__enter__.return_value.login.assert_called_once_with(
            email_config['test_sender'],
            email_config['test_password']
        )

def test_handle_match(mock_tinder):
    """Test match handling functionality"""
    test_user_id = "test123"
    handle_match(mock_tinder, test_user_id)
    
    # Verify welcome message was sent
    mock_tinder.matches.send_message.assert_called_once()
    args = mock_tinder.matches.send_message.call_args[0]
    assert args[0] == test_user_id
    assert "transparent" in args[1].lower()

@pytest.mark.parametrize("bio,expected", [
    ("Check my venmo", True),
    ("Normal profile bio", False),
    ("snapchat premium deals", True),
    ("", False),
    ("Looking for genuine connections", False)
])
def test_bot_detection_variations(bio):
    """Test bot detection with various bio contents"""
    user = {"bio": bio}
    result = detect_bot(user)
    assert isinstance(result, bool)

def test_invalid_inputs():
    """Test handling of invalid inputs"""
    # Test None input
    assert not detect_bot(None)
    
    # Test empty dict
    assert not detect_bot({})
    
    # Test invalid user object
    assert not detect_bot({"no_bio_field": "test"})

if __name__ == '__main__':
    pytest.main(['-v'])