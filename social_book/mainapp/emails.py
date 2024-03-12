from django.core.mail import send_mail
import random
from django.conf import settings

def send_otp(request, email):
    subject = 'Your OTP for registration'
    otp =   random.randint(1000, 9999)
    message = f'your otp is : {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    request.session['otp'] = otp
    
def login_detected(request, email):
    subject = 'New user Login'
    em = request.session.get('email')
    message = f'{em}, has Login on social book'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])    