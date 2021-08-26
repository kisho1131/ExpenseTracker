from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, response
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
import json

from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here


#View for User Registration
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        #get user data
        #Validate
        #Create Account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues' : request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, "Password Too Short !!")
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username= username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                # print("domain = " + domain)

                link = reverse('activate', kwargs= {'uidb64':uidb64, 'token':token_generator.make_token(user)})

                # print(link)
                activate_url = 'http://'+domain+link

                # print("=======================")
                # print(activate_url)

                emailSubject = "Active Your Account"
                emailBody = "Greeting, " + user.username + "\nPlease use the link to verify your Acoount \n" + activate_url
                email = EmailMessage(
                    emailSubject,
                    emailBody,
                    'noreply@google.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, "Account Created Successfully !! Check your Email ID to activate Account ")
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')


# Account Verification View 
class VarificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = id)
            print(user.is_active)

            # if not account_activation_token.check_token(user, token):
            #     return redirect('login' + '?Message=' + 'User Already Activated')
            
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, "Account Activated Successfully !!")
            return redirect('login')
        except Exception as ex:
            pass
        return redirect('login')
    


# Login Redirect View 
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Welcome, " + user.username + ' You are now Logged in')
                    return redirect('expenses')

                messages.error("Your Account is not verified, Please Check your mail to Verify Account") 
                return render(request, 'authentication/login.html')

            messages.error(request, "Invalid Credentials, Try Again !! ") 
            return render(request, 'authentication/login.html')

        messages.error(request, "Username and Password is Required ") 
        return render(request, 'authentication/login.html')


#View for Username Validation
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'Username should only contain Alphanumeric [(a-z)(A-Z)(0-9)] Characters'}, status = 400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error' : 'Sorry!! username is Already Taken | Choose Another'}, status = 409)
        return JsonResponse({'username_valid':True})


# Email Validation 
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error' : 'Enter Valid Email ID'}, status = 400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error' : 'Sorry!! Email is in Use'}, status = 409)

        return JsonResponse({'email_valid':True})

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You are Successfully Logged out !!")
        return redirect('login')

class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST['email']
        print("-->" + email)
        context = {
            'values' : email
        }
        if not validate_email(email):
            messages.error(request, 'Email Not Found. Enter Valid Email Address !!')
            return render(request, 'authentication/reset-password.html', context)

        domain = get_current_site(request).domain
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            emailContent = {
                'user' : user,
                'domain' : domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : PasswordResetTokenGenerator().make_token(user),
            }

            # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            # domain = get_current_site(request).domain

            # print("domain = " + domain)
            link = reverse('reset-new-password', kwargs= {'uidb64':emailContent['uid'], 'token':emailContent['token']})

            # print(link)
            reset_url = 'http://'+domain+link
            
            # print("=======================")
            # print(activate_url)

            emailSubject = "Reset Your Password-> ExpenseTracker"
            emailBody = "Greeting, " + user.username + "\nPlease use the link to Reset your Password \n" + reset_url
            email = EmailMessage(
                emailSubject,
                emailBody,
                'noreply@google.com',
                [email],
            )

            email.send(fail_silently=False)
            messages.success(request, "Follow the Link send to " + user.email + " to Reset Password !!")
            return render(request, 'authentication/login.html')

        else:
            messages.error(request, 'User Not Found. Enter Valid Email Address !!')
            return render(request, 'authentication/reset-password.html', context)

        

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64' : uidb64,
            'token' : token,
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Password Link is Invalid. Request New One!!")
                return render(request, 'authentication/reset-password.html', context)
                
        except Exception as identifire:
            pass
        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64' : uidb64,
            'token' : token,
        }
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if password1!=password2:
            messages.error(request, "Password do not Match !!")
            return render(request, 'authentication/set-new-password.html', context) 
        
        if len(password1) < 6:
            messages.error(request, "Password too Short !!")
            return render(request, 'authentication/set-new-password.html', context) 
        
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = user_id)
            user.set_password(password1)
            user.save()
            messages.success(request, "Password Reset Successfully. You can Login !!")
            return redirect('login')
        except Exception as identifire:
            messages.info(request, "Something went wrong. please Try again !!")
            return render(request, 'authentication/set-new-password.html', context)

      
        