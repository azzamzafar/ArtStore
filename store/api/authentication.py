import base64
import jwt
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
SECRET = "cockroach"


def verify_user(request):
    basic_header = request.headers.get("Authorization")
    if not basic_header:
        raise PermissionDenied("No Credentials Provided")
    basic_header_parts = basic_header.split(" ") 
    if len(basic_header_parts)!=2:
        raise PermissionDenied("Basic Authorization:format not correct!")
    if basic_header_parts[0]!="Basic":
        raise PermissionDenied("The header isnt Basic Authorization")
    credentials = basic_header_parts[1]
    email,password = str(
        base64.b64decode(credentials),'utf-8'
        ).split(':')
    return (authenticate(username=email,password=password))


def get_tokens(user):
    encoded_token = jwt.encode(
        {"id":user.id,"name":user.username},
        SECRET,
        algorithm="HS256"
    )
    return encoded_token
def verify_tokens(func):
    def inner_func(*args,**kwargs):
        request = args[0]
        jwt_header =  request.headers.get('Authorization')
        if not jwt_header:
            raise PermissionDenied("No JWT was provided")

        jwt_header_parts = jwt_header.split(" ")

        if len(jwt_header_parts)!=2:
            raise PermissionDenied("JWT Not Correct format")
        
        if jwt_header_parts[0]!="Bearer":
            raise PermissionDenied("The JWT header is not a bearer token")
       
        token = jwt_header_parts[1]
        try:
            payload = jwt.decode(token,SECRET,algorithms=["HS256"])
            return func(*args,**kwargs)
        except jwt.InvalidTokenError as e:
            raise PermissionDenied("Token Verification Failed!")
    return inner_func