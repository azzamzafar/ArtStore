from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse,HttpResponseNotAllowed,JsonResponse
from http import HTTPStatus
from django.core.exceptions import ObjectDoesNotExist
from store.api.permissions import is_admin
from store.api.authentication import verify_tokens
from store.models import Invoice
from customers_auth.models import Customer

@verify_tokens
def myorders(request):
    if request.method == "GET":
        days = request.GET.get('days','')
        invoice = None
        if days:
            try:
                orders = Invoice.objects.filter(date__gte=timezone.now()-timedelta(days=days),customer=request.user,status='captured')
                return JsonResponse(relatedobj_to_dict(orders))
            except ObjectDoesNotExist:
                return HttpResponse(status=HTTPStatus.NOT_FOUND)
        else:
            try:
                invoice = Invoice.objects.get(customer=request.user).order_by('-id').latest()
                return JsonResponse(relatedobj_to_dict(invoice))
            except ObjectDoesNotExist:
                return HttpResponse(status=HTTPStatus.NOT_FOUND)
    return HttpResponseNotAllowed(["GET"])

@verify_tokens
@is_admin
def user_orders(request):
    if request.method=="GET":
        days = request.GET.get('days','')
        email = request.GET.get('user','')
        if days and email:
            user = Customer.objects.get(email=email)
            try:
                orders = Invoice.objects.filter(date__gte=timezone.now()-timedelta(days=days),customer=user,status='captured')
                return JsonResponse(relatedobj_to_dict(orders))
            except ObjectDoesNotExist:
                return HttpResponse(status=HTTPStatus.NOT_FOUND)
        
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    return HttpResponseNotAllowed(["GET"])

# @verify_tokens
# @is_admin
# def order_count(request):
#     if request.method == "GET":
#         product = request.GET.get("product,", "")
#         if product:
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
#     return HttpResponse(status=HttpResponseNotAllowed(["GET"]))

