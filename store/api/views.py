import json
import base64
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
from store.api.authentication import verify_user, get_tokens, verify_tokens
# from store.api.validation import validate_input

def obj_to_dict(obj):
    # fields = obj.__dict__.items()
    fields = obj._meta.get_fields()
    obj_dict = {}
    
    for field in fields:
        field_Val = getattr(obj,field.name)

        if field.get_internal_type() == "ForeignKey":
            continue

        elif field.many_to_many:
            obj_dict[field.name] = field_Val.values()[0]

        elif field.get_internal_type() == "FileField" and field_Val.width:
            with open(field_Val.path,'rb') as img:
                image_data = str(base64.b64encode(img.read()),'utf-8')
                # image_data = base64img.decode('utf-8')
                obj_dict[field.name] = image_data

        else:
            obj_dict[field.name] = field_Val
    return obj_dict


def generate_tokens(request):
    user = verify_user(request)
    if user:
        token = get_tokens(user)
        return JsonResponse({'token': token})
    else:
        raise PermissionDenied("Wrong Credentials")


@verify_tokens
@csrf_exempt
def product_list(request):

    if request.method == "GET":
        products = Product.objects.all()
        products_as_dict = [obj_to_dict(p) for p in products]
        return JsonResponse({"data": products_as_dict})
    elif request.method == "POST":
        product_data = json.loads(request.body)
        product = Product.objects.create(**product_data)
        return HttpResponse(
            status=HTTPStatus.CREATED,
            headers={"Location": reverse(
                "api_product_list", args=(product.pk))},
        )
    return HttpResponseNotAllowed(["GET", "POST"])


@verify_tokens
@csrf_exempt
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "GET":
        return JsonResponse(obj_to_dict(product))

    elif request.method == "PUT" and is_admin():
        product_data = json.loads(request.body)
        for field, value in product_data.items():
            setattr(product, field, value)
        product.save()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    elif request.method == "DELETE" and is_admin():
        product.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    return HttpResponse(status=HttpResponseNotAllowed(["GET", "PUT", "DELETE"]))


