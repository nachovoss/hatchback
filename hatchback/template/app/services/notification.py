import logging
import os
from mailersend import EmailBuilder, MailerSendClient

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.api_key = os.getenv("MAILERSEND_API_KEY")
        self.from_email = os.getenv("MAILERSEND_FROM_EMAIL", "noreply@example.com")
        self.from_name = os.getenv("MAILERSEND_FROM_NAME", "Boilerplate App")
        
        if self.api_key:
            self.email_client = MailerSendClient()
        else:
            self.email_client = None
            logger.warning("MAILERSEND_API_KEY not set. Email sending will be disabled (logs only).")

    def send_email(self, to_email: str, subject: str, body: str):
        """
        Sends an email using MailerSend if configured, otherwise logs to console.
        """
        if not self.email_client:
            logger.info(f"Mock sending email to {to_email}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Body: {body}")
            return

        try:
            email = EmailBuilder()
            email.from_email(self.from_email, self.from_name)
            email.to(to_email)
            email.subject(subject)
            email.html(body)
            
            if hasattr(email, "build"):
                built_email = email.build()
                self.email_client.emails.send(built_email)
            else:
                self.email_client.emails.send(email)
                
            logger.info(f"Email sent to {to_email}")
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            raise e

    def send_password_recovery_email(self, to_email: str, token: str):
        subject = "Password Recovery"
        body = f"""
        <h1>Password Recovery</h1>
        <p>You have requested to reset your password.</p>
        <p>Use the following token to reset your password:</p>
        <pre>{token}</pre>
        <p>If you did not request this, please ignore this email.</p>
        """
        self.send_email(to_email, subject, body)

