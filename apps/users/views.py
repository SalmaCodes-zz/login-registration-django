from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import bcrypt


# Create your views here.


# '/'
def index(request):
    return render(request, 'users/index.html')


# '/success'
def success(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'users/success.html', context)


# '/process', 'POST' method that proccesses the login/registration forms.
def process(request):
    if request.method == 'POST':
        ftype = request.POST['type']
        # Registration form
        if (ftype == 'register'):
            errors = User.objects.registration_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')
            else:
                # Create User
                password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                user = User.objects.create(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    password=password_hash)
                request.session['user_id'] = user.id
                request.session['success'] = "registered"
                return redirect('/success')

        # Login form
        elif (ftype == 'login'):
            errors = User.objects.login_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')
            else: 
                user = User.objects.filter(email=request.POST['email'])
                request.session['user_id'] = user[0].id
                request.session['success'] = "loggin in"
                return redirect('/success')