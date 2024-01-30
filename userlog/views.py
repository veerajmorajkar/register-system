from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from statu import settings
from django.core.mail import send_mail

# Create your views here.
def howe(request):
    return render(request, 'index.html')

def register(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username alreasdy exists")
            return redirect('howe')

        if User.objects.filter(email=email):
            messages.error(request,"Email already exists")
            return redirect('howe')

        if len(username)>10:
            messages.error(request,"username must be under 10 characters")

        if pass1 != pass2:
            messages.error(request,"password didnt match!")        

        if not username.isalnum():
            messages.error(request,"username must be Alpha-numeric!")
            return redirect('howe')        

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request,"ACCOUNT CREATED, email sent!")
        
        subject = "welcome to login!"
        messeges = "hello " + myuser.first_name +"!! \n ThankYou"
        from_email =  settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,messages,from_email,to_list,fail_silently=True)
        return redirect('signin')

    return render(request, 'register.html')
    
def signin(request):
    
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, "index.html",{'fname':fname})
        else:
            messeges.error(request, "Bad Credentials")
            return redirect('howe')

    return render(request, 'signin.html')

def signout(request):
    logout(request)
    messages.success(request, "logged out")
    return redirect('howe')