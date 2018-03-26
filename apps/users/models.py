from __future__ import unicode_literals

from django.db import models
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        name = postData['name']
        username = postData['username']
        password = postData['password']
        password_confirmation = postData['password_confirmation']

        # Name - Required; No fewer than 3 characters
        if len(name) < 3:
            errors["name"] = "Name must be at least 3 characters."

        # Username - Required; No fewer than 3 characters; Doesn't already exist
        if len(username) < 3:
            errors["username"] = "Username must be at least 3 characters."
        else:
            data = User.objects.filter(username=username)
            if len(data) > 0:
                errors["username"] = "Username already exists, please log in."
        
        # Password - Required; No fewer than 8 characters in length; matches Password Confirmation
        if len(password) < 8:
            errors["password"] = "Password must be at least 8 characters."
        elif password != password_confirmation:
            errors["password"] = "Password confirmation must match the password."
        return errors
    
    def login_validator(self, postData):
        errors = {}
        username = postData['username']
        password = postData['password']

        data = User.objects.filter(username=username)
        # Username - Required; No fewer than 3 characters;
        if len(username) < 3:
            errors["username"] = "Username must be at least 3 characters."
        
        # Check that the user is registered
        elif len(data) == 0:
            errors["username"] = "Username does not exist. Register first!"
        
        # Make sure the password matches
        elif not bcrypt.checkpw(password.encode(), data[0].password.encode()):
            errors["password"] = "Incorrect password. Try again!"
            
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    hired_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} @{}>".format(
            self.name, self.username)


class ItemManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # Item name should be more than 3 chracters
        if len(postData['name']) < 4:
            errors['name'] = "Name should be more than 3 characters."
        return errors


class Item(models.Model):
    name = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name="added_items")
    wished_by = models.ManyToManyField(User, related_name="wished_items")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ItemManager()
    def __repr__(self):
        return "<Item object: {}>".format(self.name)
