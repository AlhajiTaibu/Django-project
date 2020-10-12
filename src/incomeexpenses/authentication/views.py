import json

from django.contrib.auth import authenticate, login, logout

from .utils import token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class UsernameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username already exists'}, status=400)

        return JsonResponse({'username_valid': True})


class EmailValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email already exists'}, status=400)

        return JsonResponse({'email_valid': True})


class RegistrationView(View):

    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, 'Password too short')
                    context = {'username': username,
                               'email': email,
                               'password': password}
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                reverse_link = reverse('verify-email', kwargs={
                    'uidb64': uidb64,
                    'token': token
                })
                url = 'http://' + current_site + reverse_link

                email_body = f'Hi ' + user.username + ', \nPlease, kindly use the link below to activate your account \n' + url
                email_subject = 'Activate your account'
                email = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    to=[email]
                )
                EmailThread(email).start()
                # email.send(fail_silently=False)
                messages.success(request, 'Registration success, kindly visit your confirm your email')
                return render(request, 'authentication/register.html')
            else:
                messages.error(request, 'email already exists')
                context = {'username': username,
                           'email': email,
                           'password': password}
                return render(request, 'authentication/register.html', context)
        else:
            messages.error(request, 'username already exists')
            context = {'username': username,
                       'email': email,
                       'password': password}
            return render(request, 'authentication/register.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, id=id)
            if not token_generator.check_token(user, token):
                messages.info(request, 'user already activated')
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as e:
            pass


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        context = {
            'fields': request.POST
        }
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome {username}')
                    return redirect('index')
                else:
                    messages.error(request, 'Account inactive')
                    return render(request, 'authentication/login.html', context)
            else:
                messages.error(request, 'Account does not exists')
                return render(request, 'authentication/login.html', context)
        else:
            messages.error(request, 'Please fill all fields')
            return render(request, 'authentication/login.html', context)


class LogOutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You have being logged out')
        return redirect('login')