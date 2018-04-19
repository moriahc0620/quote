from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'first_app/index.html')

def register(request):
    print request.POST
    result = User.objects.val_reg(request.POST)
    if result[0]:
        request.session['user_id'] = result[1].id
        request.session['email'] = result[1].email
        return redirect('/quotes')
    else:
        for error in result[1]:
            messages.add_message(request,messages.INFO, error)

        return redirect('/')

def login(request):
    result = User.objects.val_log(request.POST)
    if result[0]:
        request.session['user_id'] = result[1].id
        request.session['email'] = result[1].email
        return redirect('/quotes')
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)

        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def quotes(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'my_favorite_quotes': user.favorite_quotes.all(),
        'my_added_quotes': user.added_quotes.all(),
        'others_quotes': Quote.objects.exclude(favorite=user).exclude(quotable=user)
    }
    return render(request, 'first_app/quotes.html', context)

def add_to_list(request, quote_id): # feature form for adding to my list
    this_user = User.objects.get(id=request.session['user_id'])
    this_quote = Quote.objects.get(id=quote_id)
    this_quote.quotable.add(this_user)
    return redirect('/quotes')

def remove_from_list(request, quote_id): # feature to remove from my favorites
    this_user = User.objects.get(id=request.session['user_id'])
    this_quote = Quote.objects.get(id=quote_id)
    this.quote.quotable.remove(this_user)
    return redirect('/quotes')

def contribute_quote(request):
    errors = Quote.objects.val_quote(request.POST)
    if len(errors) > 0:
        for error in errors:
            messages.add_message(request, messages.INFO, error)
        return redirect('/quotes')
    else:
        quotes = Quote.objects.create(
            quoted_by=request.POST['quoted_by'],
            message=request.POST['message'],
            favorite=User.objects.get(id=request.session['user_id'])
        )
        return redirect('/quotes')

def other_users(request, trip_id):
    context = {
        'quote':Quote.objects.get(id=quote_id)
    }
    return render(request, 'quotes/other_users.html', context)

        





