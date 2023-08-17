from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages # It is used to sent messages
from django.http import HttpResponse
from .models import Profile

# Landing Page

def index(request):
    return render(request, 'index.html')

# User Authentication

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        print(username, email)

        if password == password2:
            if User.objects.filter(email=email).exists(): # email is alresdy exist or not in the database
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:   # if the email and username doesnot exists in the db then it will create newly and add it to the db
                user =User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in and redirect to settings page
                # create a profile for the new user 

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password= request.POST['password']

        user = auth.authenticate(username= username, password=password)

        if user is not None: # if the user name is present in DB
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('signin')
        
    else:
        return render(request, 'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('signin')