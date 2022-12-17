import json
from http import HTTPStatus
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from store.models import Product
from store.api.permissions import (
    has_permissions,
    has_object_permissions,
    is_admin,
)
from store.api.authentication import verify_user,get_tokens,verify_tokens


def obj_to_dict(obj):
    fields = obj.__dict__.items()
    obj_dict = {}
    for field,val in fields:
        if field!='_state':
            obj_dict[field]=val
    return obj_dict

def generate_tokens(request):
    user = verify_user(request)
    if user:
        token = get_tokens(user)
        return JsonResponse({'token':token})
    else:
        raise PermissionDenied("Wrong Credentials")

   
@verify_tokens
@csrf_exempt
def product_list(request):

    if request.method == "GET":
        products = Product.objects.all()
        products_as_dict = [obj_to_dict(p) for p in products]
        return JsonResponse({"data":products_as_dict})
    elif request.method == "POST":
        product_data = json.loads(request.body)
        product = Product.objects.create(**product_data)
        return HttpResponse(
            status = HTTPStatus.CREATED,
            headers={"Location":reverse("api_product_list",args=(product.pk))},
        )
    return HttpResponseNotAllowed(["GET","POST"])

@verify_tokens
@csrf_exempt
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
        
    if request.method == "GET":
        return JsonResponse(obj_to_dict(product))
    
    elif request.method == "PUT" and is_admin():
        product_data = json.loads(request.body)
        for field, value in product_data.items():
            setattr(product,field,value)
        product.save()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    
    elif request.method == "DELETE" and is_admin():
        product.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    return HttpResponse(status=HttpResponseNotAllowed(["GET","PUT","DELETE"]))
    

