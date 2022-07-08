from functools import wraps
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate

def log_out(url):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return function(request,*args,**kwargs)
               
            else:
                return redirect(url)

        return wrap
    return decorator