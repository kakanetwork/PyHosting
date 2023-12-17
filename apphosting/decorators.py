# decorators.py

from django.shortcuts import redirect
from functools import wraps

def login_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_flag = request.session.get('user_flag')
        if user_flag == 'A':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('erro_autorizacao')
    return _wrapped_view

def login_admindominio(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_flag = request.session.get('user_flag')
        if user_flag == 'D':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('erro_autorizacao')
    return _wrapped_view

def login_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_flag = request.session.get('user_flag')
        if user_flag == 'U':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('erro_autorizacao')
    return _wrapped_view
