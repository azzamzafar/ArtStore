import json
from http import HTTPStatus
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from store.api.serializers import obj_to_dict
from store.models import Product, Cart, Invoice
from store.api.permissions import (
    is_admin,
)
from store.api.authentication import verify_user, get_tokens, verify_tokens
# from django.core.exceptions import ObjectDoesNotExist




def generate_tokens(request):
    user = verify_user(request)
    if user:
        token = get_tokens(user)
        return JsonResponse({"token": token})
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
            headers={"Location": reverse("api_product_list", args=(product.pk))},
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

@verify_tokens
@is_admin
def product_stats(request,pk):
    if request.method=="GET":
        carts_count = Cart.objects.filter(
            items__product_id=pk).distinct().count()
        orders_count = Invoice.objects.filter(
            orders__product_id=pk,status='captured'
        ).distinct().count()
        return JsonResponse({'prod_in_carts':carts_count,'orders_count':orders_count})
    return HttpResponse(status=HttpResponseNotAllowed(["GET", "PUT", "DELETE"]))