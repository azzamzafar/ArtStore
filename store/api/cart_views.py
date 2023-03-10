from django.http import HttpResponse,HttpResponseNotAllowed,JsonResponse
from http import HTTPStatus
from django.core.exceptions import ObjectDoesNotExist
from store.api.permissions import is_admin
from store.api.authentication import verify_tokens
from store.api.serializers import obj_to_dict
from store.models import Cart
from customers_auth.models import Customer


@verify_tokens
def mycart(request):
    if request.method == "GET":
        try:
            cart = Cart.objects.get(customer=request.user)
            return JsonResponse(obj_to_dict(cart))
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
                cart_dict = [obj_to_dict(c) for c in carts]    
                return JsonResponse({'data':cart_dict})
            except ObjectDoesNotExist:
                return HttpResponse(status=HTTPStatus.NOT_FOUND)
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    return HttpResponseNotAllowed(["GET"])
