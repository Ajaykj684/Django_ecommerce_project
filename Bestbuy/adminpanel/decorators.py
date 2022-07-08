from functools import wraps
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

def log(url):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                if user.is_admin == True:
                    return function(request,*args,**kwargs)
                else:

                    return redirect(url)
            else:
                return redirect(url)

        return wrap
    return decorator