import unittest
from unittest.mock import patch
from api.models.patient_model import Patient
from api.notification_senders.email_sender import EmailSender
import io

class TestEmailSender(unittest.TestCase):

    @patch('api.notification_senders.email_sender.smtplib.SMTP')
    @patch('api.notification_senders.email_sender.os.getenv')
    def test_send_notification_success(self, mock_getenv, mock_smtp):
        mock_getenv.side_effect = lambda key: 'test@example.com' if key == 'EMAIL_USER' else 'password'
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        patient = Patient(email_address='patient@example.com')
        message = 'Test message'
        email_sender = EmailSender()

        email_sender.send_notification(patient, message)

        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with('test@example.com', 'password')
        mock_smtp_instance.sendmail.assert_called_once_with(
            'test@example.com',
            'patient@example.com',
            unittest.mock.ANY
        )

    @patch('api.notification_senders.email_sender.smtplib.SMTP')
    @patch('api.notification_senders.email_sender.os.getenv')
    def test_send_notification_failure(self, mock_getenv, mock_smtp):
        mock_getenv.side_effect = lambda key: 'test@example.com' if key == 'EMAIL_USER' else 'password'
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        mock_smtp_instance.sendmail.side_effect = Exception('SMTP error')
        patient = Patient(email_address='patient@example.com')
        message = 'Test message'
        email_sender = EmailSender()
        email_sender.send_notification(patient, message)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            email_sender.send_notification(patient, message)
            printed_output = mock_stdout.getvalue()
        self.assertIn('Failed to send email: SMTP error', printed_output)

if __name__ == '__main__':
    unittest.main()