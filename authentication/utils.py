from django.core.mail import EmailMessage
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        from_email = 'info@mentorhub.com'

        # Create an EmailMessage with content_subtype set to 'html'
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],  # The email body (HTML content)
            to=[data['to_email']],
            from_email=from_email,
        )

        # Set the content_subtype to 'html'
        email.content_subtype = 'html'

        # Create an instance of EmailThread with the email
        email_thread = EmailThread(email)

        # Start the email thread to send the email asynchronously
        email_thread.start()

        # Note that this function returns immediately, and the email is sent in the background.
