import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from mail_logic import (
    initial, send_mail, generate_html_email, 
    send_monthly_email, send_weekly_email, send_daily_expired_email
)

@pytest.fixture
def mock_collection():
    return MagicMock()

@patch('mail_logic.Mongo.MongoDBHandler')
def test_initial(mock_mongo):
    mock_handler = MagicMock()
    mock_mongo.return_value = mock_handler
    mock_collection = MagicMock()
    mock_handler.get_expiry_info_collection.return_value = mock_collection

    result = initial()
    assert result == mock_collection

@patch('mail_logic.smtplib.SMTP')
def test_send_mail(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    send_mail("Test Subject", "Test Body")

    mock_server.login.assert_called_once()
    mock_server.sendmail.assert_called_once()

def test_generate_html_email():
    result = generate_html_email("expired", ["Category1", "Category2"], 2)
    assert "Category1" in result
    assert "Category2" in result
    assert "Total expired files: 2" in result

@patch('mail_logic.initial')
@patch('mail_logic.send_mail')
def test_send_monthly_email(mock_send_mail, mock_initial, mock_collection):
    mock_initial.return_value = mock_collection
    current_date = datetime.now()
    mock_collection.find.return_value = [
        {"Category": "Test1", "expires": True, "expiry_date": current_date + timedelta(days=15)},
        {"Category": "Test2", "expires": True, "expiry_date": current_date + timedelta(days=40)}
    ]

    send_monthly_email()

    mock_send_mail.assert_called_once()
    args = mock_send_mail.call_args[0]
    assert "Files Expiring in One Month!!!" in args[0]
    assert "Test1" in args[1]
    assert "Test2" not in args[1]

@patch('mail_logic.initial')
@patch('mail_logic.send_mail')
def test_send_weekly_email(mock_send_mail, mock_initial, mock_collection):
    mock_initial.return_value = mock_collection
    current_date = datetime.now()
    mock_collection.find.return_value = [
        {"Category": "Test1", "expires": True, "expiry_date": current_date + timedelta(days=5)},
        {"Category": "Test2", "expires": True, "expiry_date": current_date + timedelta(days=6)}
    ]

    send_weekly_email()

    mock_send_mail.assert_called_once()
    args = mock_send_mail.call_args[0]
    assert "Files Expiring in One Week!!!" in args[0]
    print("Generated HTML content:")
    print(args[1])
    assert "Test1" in args[1]
    assert "Test2" in args[1]


@patch('mail_logic.initial')
@patch('mail_logic.send_mail')
def test_send_daily_expired_email(mock_send_mail, mock_initial, mock_collection):
    mock_initial.return_value = mock_collection
    current_date = datetime.now()
    mock_collection.find.return_value = [
        {"Category": "Test1", "expires": True, "expiry_date": current_date - timedelta(days=1)},
        {"Category": "Test2", "expires": True, "expiry_date": current_date + timedelta(days=1)}
    ]

    send_daily_expired_email()

    mock_send_mail.assert_called_once()
    args = mock_send_mail.call_args[0]
    assert "Expired Files Notification!!!" in args[0]
    assert "Test1" in args[1]
    assert "Test2" not in args[1]
