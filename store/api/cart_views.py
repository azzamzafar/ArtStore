from django.http import HttpResponse,HttpResponseNotAllowed,JsonResponse
from http import HTTPStatus
from django.core.exceptions import ObjectDoesNotExist
from store.api.permissions import is_admin
from store.api.authentication import verify_tokens
from store.models import Cart
from customers_auth.models import Customer


@verify_tokens
def mycart(request):
    if request.method == "GET":
        try:
            cart = Cart.objects.get(customer=request.user)
            return JsonResponse(relatedobj_to_dict(cart))
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.NOT_FOUND)
    return HttpResponseNotAllowed(["GET"])

@verify_tokens
@is_admin
def user_carts(request):
    if request.method == "GET":
        email = request.GET.get('user','')
        if email:
            user = None
            try:
                user = Customer.objects.get(email=email)
                carts = Cart.objects.get(customer=user)
                return JsonResponse(relatedobj_to_dict(carts))
            except ObjectDoesNotExist:
                return HttpResponse(status=HTTPStatus.NOT_FOUND)
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    return HttpResponseNotAllowed(["GET"])
# @verify_tokens
# @is_admin
# def cart_count(request):
#     ...
#     if request.method == "GET":
#         product = request.GET.get("product", "")
#         if product != "":
#             try:
#                 return (
#                     Cart.objects.filter(user_items__product_id=product)
#                     .distinct()
#                     .count()
#                 )
#             except ObjectDoesNotExist:
#                 return HttpResponse(status=HTTPStatus.BAD_REQUEST)
#         else:
#             return HttpResponse(status=HTTPStatus.BAD_REQUEST)
#     return HttpResponse(status=HttpResponseNotAllowed(["GET", "PUT", "DELETE"]))
