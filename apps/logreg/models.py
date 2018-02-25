# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, first, last, email, dob, password, confirm):
        response = {
            "valid": True,
            "errors": [],
            "user": None
        }
# check to see if variables work
        x = first
        y = last

        if len(first) < 1:
            response['errors'].append('First name cannot be empty')
        elif len(first) < 2:
            response['errors'].append('Name must be at least 2 characters')
        # check if this line works
        elif x.isalpha() == False:
            response['errors'].append('First name can only contain letters')
        
        if len(last) < 1:
            response['errors'].append('Last name cannot be empty')
        elif len(last) < 2:
            response['errors'].append('Last Name must be at least 2 characters')
        elif y.isalpha() == False:
            response['errors'].append('Last name can only contain letters')

        if len(email) < 1:
            response['errors'].append('Email cannot be empty')
        elif not EMAIL_REGEX.match(email):
            response['errors'].append('Invalid email')
        else:
            email_list =User.objects.filter(email=email.lower())
            if len(email_list) > 0:
                response['errors'].append('Email already in use')

        if len(dob) < 1:
            response['errors'].append('What is your REAL birthday?')
        else:
            date = datetime.strptime(dob, '%Y-%m-%d')
            today = datetime.now()
            if date > today:
                response['errors'].append('You are not a future baby')

        if len(password) < 1:
            response['errors'].append('Password cannot be empty')           
        elif len(password) < 8:
            response['errors'].append('Password must be at least 8 characters')

        if len(confirm) < 1:
            response['errors'].append('Please confirm password')
        elif confirm != password:
            response['errors'].append('Passwords must match')

        if len(response['errors']) > 0:
            response['valid'] = False
        else:
            response['user'] = User.objects.create(
                first=first,
                last=last,
                email=email.lower(),
                dob=date,
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )
        return response

    def login(self, email, password):
        response = {
            "valid": True,
            "errors": [],
            "user": None
        }

        if len(email) < 1:
            response['errors'].append('Email cannot be empty')
        elif not EMAIL_REGEX.match(email):
            response['errors'].append('Invalid email')
        else:
            email_list = User.objects.filter(email=email.lower())
            if len(email_list) == 0:
                response['errors'].append('No matching email')

        if len(password) < 1:
            response['errors'].append('Password cannot be empty')           
        elif len(password) < 8:
            response['errors'].append('Password must be at least 8 characters')

        if len(response['errors']) == 0:
            hashed_pw = email_list[0].password
            if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
                response['user'] = email_list[0]
            else:
                response['errors'].append('Incorrect password')
        
        if len(response['errors']) > 0:
            response['valid'] = False
        
        return response


class User(models.Model):
    first = models.CharField(max_length=255)
    last = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    # django belt review pt 1 13:00
 
 
# class Message(models.Model):
#     content = models.TextField(max_length=1000)
#     sent_by = models.ForeignKey(User, related_name="sent_messages")
#     recieved_by = models.ForeignKey(User, related_name="received_messages")
#     created_at = models.DateTimeField(auto_now_add=True)
#     objects = MessageManager()
