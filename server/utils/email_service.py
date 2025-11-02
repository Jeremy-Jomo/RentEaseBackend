import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from server.config import Config

def send_email(to_email, subject, html_content):
    """
    Send an email using SendGrid.
    """
    message = Mail(
        from_email=Config.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        print("DEBUG SENDGRID KEY PRESENT:", bool(Config.SENDGRID_API_KEY))
        print(f"📤 Sending email to: {to_email} ...")
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✅ Email sent to {to_email}. Status: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return None
