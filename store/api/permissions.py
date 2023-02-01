from http import HTTPStatus
from django.http import HttpResponse

def is_admin(func):
    def inner_func(*args,**kwargs):
        request = args[0]
        if request.user and request.user.is_staff:
            return func(*args,**kwargs)
        else:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)
    return inner_func

def has_permissions(func):
    def inner_func(*args,**kwargs):
        request = args[0]
        if request.method in ["GET","HEAD"]:
            return func(*args,**kwargs)
        elif request.user and request.user.is_authenticated:
            return func(*args,**kwargs)
    return inner_func

def has_object_permissions(request,obj):
    if request.method in ["GET","HEAD"]:
        return True
    else:
        return request.user==obj.author

def owner_or_admin(func):
    def inner_func(*args,**kwargs):
        request = args[0]
        object = kwargs[0]
        if is_admin(request) or request.user==object.author:
            return func(*args,**kwargs)
        else:
            return None
    return inner_func