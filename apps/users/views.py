from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import bcrypt


# Create your views here.


# '/' OR '/main': Shows login/registration page.
def index(request):
    return render(request, 'users/index.html')


# '/dashboard': Shows dashboard page.
def dashboard(request):
    if ('user_id' not in request.session.keys()):
        return redirect('/main')

    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'other_wishlist': Item.objects.all().exclude(wished_by=user)
    }
    return render(request, 'users/dashboard.html', context)


# '/process': 'POST' method that proccesses the login/registration forms.
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
                    name=request.POST['name'],
                    username=request.POST['username'],
                    hired_date=request.POST['hired_date'],
                    password=password_hash)
                request.session['user_id'] = user.id
                return redirect('/dashboard')

        # Login form
        elif (ftype == 'login'):
            errors = User.objects.login_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')
            else: 
                user = User.objects.filter(username=request.POST['username'])
                request.session['user_id'] = user[0].id
                return redirect('/dashboard')


# '/add_item': 'POST' method that creates a new item.
def add_item(request):
    if request.method == 'POST':
        errors = Item.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/wish_items/create')
        else:
            # Create Item
            user = User.objects.get(id=request.session['user_id'])
            item = Item.objects.create(name=request.POST['name'], added_by=user)
            item.wished_by.add(user)
            return redirect('/dashboard')


# '/wish_items/<id>'
def show_item(request, id):
    context = {
        'item': Item.objects.get(id=id)
    }
    return render(request, 'users/show_item.html', context)


# '/wish_items/<id>/delete': Deletes the item.
def delete_item(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('/dashboard')


# '/wish_items/create', displays the create form page.
def create_item(request):
    return render(request, 'users/create_item.html')


# '/wishlist_add/<id>': Adds the item with <id> to current user's wishlist.
def wishlist_add(request, id):
    item = Item.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    item.wished_by.add(user)
    return redirect('/dashboard')


# '/wishlist_remove/<id>': Removes the item with <id> from current user's wishlist.
def wishlist_remove(request, id):
    item = Item.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    item.wished_by.remove(user)
    return redirect('/dashboard')

    
# '/logout'
def logout(request):
    request.session.pop('user_id')
    return redirect('/main')