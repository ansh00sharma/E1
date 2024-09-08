from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from project.settings import EMAIL_HOST_PASSWORD
from django.core.mail import EmailMessage
from project import settings

def detectUser(user):
    if user.role == 1:
        redirecturl = 'vendorDashboard'
        return redirecturl
    elif user.role == 2:
        redirecturl = 'customerDashboard'
        return redirecturl
    elif user.role == None and user.is_superadmin:
        redirecturl = '/admin'
        return redirecturl    

def send_verification_email(request, user,mail_subject,email_template):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL 
        current_site = get_current_site(request)
        message = render_to_string(email_template,{
            'user':user,
            'domain':current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        })
        to_email = user.email
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.content_subtype = "html"
        mail.send()
        
    except Exception as e:
        print(e)

def send_notification(mail_subject,mail_template,context):
    print(f"sending email to {context['to_email']}")
    from_email = settings.DEFAULT_FROM_EMAIL 
    message = render_to_string(mail_template,context)
    if(isinstance(context['to_email'],str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email,bcc=[context['domain']])
    mail.send()      
    print(f"email send successfully to {to_email}") 


