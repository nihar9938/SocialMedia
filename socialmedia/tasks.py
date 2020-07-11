
#Used for Celery
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.decorators import task

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

@task
def Sendmail(email, msg):
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    html = get_template("mail.html").render({"msg":msg})
    #html = "<h1>Email</h1>"
    sub = "Thank you For your Registration on Social on"
    send_mail(sub, " ", from_email, to_email, html_message=html)


