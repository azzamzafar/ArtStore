
def has_permissions(request):
    if request.method in ["GET","HEAD"]:
        return True
    else:
        return bool(request.user and request.user.is_authenticated)
def has_object_permissions(request,obj):
    ...
    if request.method in ["GET","HEAD"]:
        return True
    else:
        return request.user==obj.author

def is_admin(request):
    return bool(request.user and request.user.is_staff)