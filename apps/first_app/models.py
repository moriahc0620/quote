from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def val_reg(self, postData):
        print postData
        errors = []
        name = postData['name']
        alias = postData['alias']
        email = postData['email']
        password = postData['password'] # at least 8 characters
        c_password = postData['c_password']

        if len(name) is 0:
            errors.append('Name is required')
        elif len(name) < 3:
            errors.append('Name must be at least 3 characters')
        if len(alias) is 0:
            errors.append('Alias is required')
        elif len(alias) < 3:
            errors.append('Alias must be at least 3 characters')
        if len(email) is 0:
            errors.append('Email is required')
        if len(password) is 0:
            errors.append('Password is required')
        elif password != c_password:
            errors.append('Passwords must match')

        if len(errors) > 0:
            return (False, errors)
        else:
            result = self.filter(email=email)
            if len(result) > 0:
                errors.append('Email already exists')
                return (False, errors)
            else:
                new_user = self.create(
                    name = name,
                    email = email,
                    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                )
                return (True, new_user)

    def val_log(self, postData):
        errors = []
        password = postData['password']
        email = postData['email']
        if len(password) is 0:
            errors.append('Password is required')
        if len(email) is 0:
            errors.append('Email is required')
        if len(errors) > 0:
            return (False, errors)
        else:
            result = self.filter(email=email)
            if len(result) > 0:
                user = result[0]
                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    return (True, user)
                else:
                    errors.append('Invalid email/password combo')
                    return (False, errors)
            else:
                errors.append('Invalid email/password combo')
                return (False, errors)

class QuoteManager(models.Model):
    def val_quote(self, postData):
        errors = []
        if len(quoted_by) is 0:
            errors.append('Quoted By is required before submitting')
        elif len(quoted_by) < 3:
            errors.append('Quoted By must be at least 3 characters')
        if len(message) is 0:
            errors.append('Message is required before submitting')
        elif len(message) < 10:
            errors.append('Message must be at least 10 characters')

        if len(errors) > 0:
            return (False, errors)

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    favorite = models.ForeignKey(User, related_name="favorite_quotes")
    quotable = models.ManyToManyField(User, related_name="added_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()



