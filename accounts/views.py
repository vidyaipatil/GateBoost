from django.shortcuts import render, redirect, reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from django.http import HttpResponse
from . import models
from django.contrib import messages
# Create your views here.

def send_email(username, recipient_mail):
    subject = "Welcome to Gateboost!"
    body = "Hello " + username + ", thank you for signing up! Visit gateboost.com for excelling in your GATE preparation."
    from_mail = "Team Gateboost"
    to_mail = [recipient_mail,]

    send_mail(subject, body, from_mail, to_mail, fail_silently = False)

def register(request):

    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        password = request.POST.get('password')
        year = request.POST.get('year')
        branch = request.POST.get('branch')

        # password = make_password(password)

        try:
            user = get_user_model().objects.create_user(username = username, email=email, first_name = fname, last_name = lname, password = password)

        except IntegrityError:
            
            text = "Username already exists"
            return render(request,'accounts/register.html',{'exists_text':text,})
        user.save()
        
        

        userinfo = models.UserInfo.objects.create(user=user, year = year, branch = branch)
        userinfo.save()
        messages.add_message(request, messages.INFO, 'Registered successfully!')

        try:
            login(request,user)
            send_email(user.first_name, user.email)
        except TimeoutError as error:
            context = {
                'error':str(error)
            }
            return render(request, 'boost/errors.html', context)


        homepage = reverse('boost:homepage')
        return redirect(homepage)
    else:
        return render(request,'accounts/register.html',{})


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from boost import urls
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # password = make_password(password) 

        user = authenticate(request,username = username,
                            password = password)
        
        # print(username, password, user)
        if user and user.check_password(password):
            if user.is_active:
                login(request,user)
                
                homepage = reverse('boost:homepage')
                return redirect(homepage)
            else:
                return render(request,'accounts/login.html',{'error':'User is inactive!'})
        else:
            # messages.error
            # messages.error(request, 'Wrong username or password')
            return render(request,'accounts/login.html',{'error':'Login credentials not matching!'})

        


    else:
        return render(request,'accounts/login.html',{})
 
def forget_pass(request):
    if request.method == "POST":
        email = request.POST.get('email')
        

        try:
            user = models.User.objects.get(email=email)
            subject = "Gateboost Password"
            body = "Hello " + user.first_name + ", your Gateboost password is - " + user.password + ". Use this password to login into Gateboost. Change the password if required in profile."
            from_mail = "Team Gateboost"
            to_mail = [user.email,]
            send_mail(subject, body, from_mail, to_mail, fail_silently = False)
            return redirect(reverse('accounts:login'))
                           

        except models.User.DoesNotExist :
            return render(request, 'accounts/forgetpassword.html',{'error':"Sorry! The email is not registered with us."})

            



        
            

    return render(request, 'accounts/forgetpassword.html',{})


@login_required 
def user_logout(request):
    logout(request)
    return redirect(reverse('boost:homepage'))