import unittest
from unittest.mock import patch, MagicMock
from api.notification_senders.notifications_handler import get_senders, handle_notifications
from api.models.patient_model import Patient
from fastapi import BackgroundTasks
from api.notification_senders.email_sender import EmailSender

class TestNotificationsHandler(unittest.TestCase):

    def test_get_senders(self):
        senders = get_senders()
        self.assertEqual(len(senders), 1)
        self.assertIsInstance(senders[0], EmailSender)

    @patch('api.notification_senders.notifications_handler.EmailSender')
    def test_handle_notifications(self, MockEmailSender):
        mock_sender = MockEmailSender.return_value
        mock_sender.send_notification = MagicMock()
        
        patient = Patient(name="John Doe")
        background_tasks = BackgroundTasks()
        background_tasks.add_task = MagicMock()

        handle_notifications(patient, background_tasks)

        background_tasks.add_task.assert_called_once_with(
            mock_sender.send_notification, patient, "Thank you for registering, John Doe!"
        )

if __name__ == '__main__':
    unittest.main()