from kavenegar import *
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from searchengine import settings


class Email:
    @staticmethod
    def send_email(title, body, email):
        EmailMessage(
            subject=title,
            body=body,
            from_email=settings.DEFAULT_EMAIL,
            to=[email, ],
        ).send()

    @staticmethod
    def send_active_search_result(subject, url, to):
        html_content = render_to_string(
            'active_search_result_template.html', {'url': url}
        )  # render with dynamic value
        text_content = strip_tags(
            html_content
        )  # Strip the html tag. So people can see the pure text at least.
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_EMAIL,
            [to, ]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class KavenegarSMS:

    def __init__(self):
        self.api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

    def register(self, receptor=None, code=None, password=None):
        self.params = {
            'receptor': receptor,
            'template': 'zaris-register',
            'token': code,
            'type': 'sms'
        }

    def car_request_notif(self, receptor=None, applicant=None):
        self.params = {
            'receptor': receptor,
            'template': 'car-request-notif',
            'token': applicant,
            'type': 'sms'
        }

    def send(self):
        flag = True
        for i, j in self.params.items():
            if j is None:
                flag = False
        if flag:
            try:
                return self.api.verify_lookup(self.params)
            except APIException as e:
                return e
            except HTTPException as e:
                return e
        else:
            raise APIException
