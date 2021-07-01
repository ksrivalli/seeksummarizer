from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect("/")
def forgot(request):
    if request.method=='POST':
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        
        if User.objects.filter(username=username).exists():
            if password1==password2:
                u = User.objects.get(username=username)
                u.set_password(password1)
                u.save()
                return redirect('login')
            else:
                messages.info(request,'Passwords are not matching')
                return redirect('forgot')
        else:
            messages.info(request,'Username doesnt exist')
            return redirect('forgot')
        return redirect('login')
    else:
        return render(request,"forgot.html")

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']

        if password1==password2:
        	if User.objects.filter(username=username).exists():
        		messages.info(request,'Username taken')
        		return redirect('register')
        	elif User.objects.filter(email=email).exists():
        		messages.info(request,'Email taken')
        		return redirect('register')
        	else:
        		user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
        		user.save()
        		print('user saved')
        		return redirect('login')
        else:
        	messages.info(request,'Passwords not matching')
        	return redirect('register')
        return redirect('login')
    else:
    	return render(request,"register.html")