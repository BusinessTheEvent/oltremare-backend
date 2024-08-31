from io import StringIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import jinja2
from src.config import settings

def gmail_send_mail_to(recipient: str, subject: str, attachment: StringIO = None, attachment_filename: str = None, **kwargs):
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_PASSWORD

    ## render custom email template
    with open("email_template.html") as file:
        body_html = file.read()
    body_html = jinja2.Template(body_html).render(kwargs)

    try:
        
        # Create the email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient

        # Attach the HTML body to the email
        msg.attach(MIMEText(body_html, "html"))

      # Attach the file if provided
        if attachment:
            if attachment_filename is None:
                raise ValueError("attachment_filename must be provided if attachment is provided")
            
            attachment.seek(0)  # Ensure the cursor is at the beginning of the file
            part = MIMEApplication(attachment.read(), Name=attachment_filename)
            part['Content-Disposition'] = f'attachment; filename="{attachment_filename}"'
            msg.attach(part)

        try:
            # Connect to the Gmail SMTP server
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password.get_secret_value())
                server.sendmail(sender_email, recipient, msg.as_string())
            print("Email sent successfully")

        except smtplib.SMTPException as error:
            print(f"An error occurred: {error}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# if __name__ == "__main__":
#     recipient="mario@yopmail.com"
#     subject="Test email"

#     gmail_send_mail_to(recipient=recipient, subject=subject, title="Title", text="Body")
