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

        # Send the email
        email.send()
