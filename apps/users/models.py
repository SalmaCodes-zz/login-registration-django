from __future__ import unicode_literals

from django.db import models
import bcrypt, md5, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        fname = postData['first_name']
        lname = postData['last_name']
        email = postData['email']
        password = postData['password']
        password_confirmation = postData['password_confirmation']

        # First Name - Required; No fewer than 2 characters; letters only
        if len(fname) < 2:
            errors["first_name"] = "First name must be at least 2 characters."
        elif not fname.isalpha():
            errors["first_name"] = "First name must be letters only."
        
        # Last Name - Required; No fewer than 2 characters; letters only
        if len(lname) < 2:
            errors["last_name"] = "Last name must be at least 2 characters."
        elif not lname.isalpha():
            errors["last_name"] = "Last name must be letters only."

        # Email - Required; Valid Format; Doesn't already exist
        if len(email) < 1:
            errors["email"] = "Email cannot be empty!"
        elif not EMAIL_REGEX.match(email):
            errors["email"] = "Invalid Email Address!"
        data = User.objects.filter(email=email)
        if len(data) > 0:
            errors["email"] = "Email already exists, please log in."
        
        # Password - Required; No fewer than 8 characters in length; matches Password Confirmation
        if len(password) < 8:
            errors["password"] = "Password must be at least 8 characters."
        elif password != password_confirmation:
            errors["password"] = "Password confirmation must match the password."
        return errors
    
    def login_validator(self, postData):
        errors = {}
        email = postData['email']
        password = postData['password']

        # Email - Required; Valid Format
        if len(email) < 1:
            errors["email"] = "Email cannot be empty!"
        elif not EMAIL_REGEX.match(email):
             errors["email"] = "Invalid Email Address!"
        
        # Check that the user is registered
        data = User.objects.filter(email=email)
        elif len(data) == 0:
            errors["email"] = "Email does not exist. Register first!"
        
        # Make sure the password matches
        elif not bcrypt.checkpw(password.encode(), data[0].password.encode()):
            errors["password"] = "Incorrect password. Try again!"
            
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {}, {}>".format(
            self.first_name, self.last_name, self.email)