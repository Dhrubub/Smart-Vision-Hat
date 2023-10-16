from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def send_email():
    sg = SendGridAPIClient('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')
    email = Mail(
        from_email='mlfdb2023@gmail.com',
        to_emails='cxw8848@hotmail.com', #'smartvisionhat@gmail.com',
        subject='Emergency Alert from Smart Vision Hat',
        html_content='<strong>You have a new alert from your contact \n by Smart Vision Hat</strong>'
    )
    response = sg.send(email)
    print(response.status_code)

send_email()
