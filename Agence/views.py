from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import time

def home(request):
    return render(request,'home.html')

def log_in(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('contest')
            else:
                print("Mdp incorrect")
        else:
            print("L'utilisateur n'existe pas")

        print("=="*5, " NEW POST: ", email,password, "=="*5)
    return render(request,'login.html', {})


def register(request):
    error = False
    message = ""
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None) 

        try:
            validate_email(email)
        except:
            error = True
            message = "Entrez un mail valide."
    
        if error == False:
            if password != repassword:
                error = True
                message = "Les mdp ne correspondent pas"
        
        print("=="*5, " NEW POST: ",name,email,password, "=="*5)

        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"L'email : {email} ou le pseudo {name} est déjà utilisé"
 
        if error == False:
            user = User(
                username = name,
                email = email,
            )
            user.save()
            user.password = password
            user.set_password(user.password)
            user.save()
            return redirect('login')

            print("=="*5, " NEW POST: ",name,email,password, "=="*5)

    context = {
        'error':error,
        'message':message
    }
    return render(request,'register.html', context)


@login_required(login_url='contest')
def contest(request):
    return render(request, 'contest.html', {})

def log_out(request):
    return(request, 'login.html', {})