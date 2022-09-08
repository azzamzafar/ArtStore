from ast import Or
from operator import ge
from typing import OrderedDict
from urllib import response
from django.db import DatabaseError
from django.http import HttpResponseBadRequest
from django.shortcuts import render,redirect
import razorpay
from django.views.decorators.csrf import csrf_exempt
import hmac,hashlib
# Create your views here.

def generate_signature(order_id,payment_id,key):
    msg = order_id+"|"+payment_id

    signature = hmac.new(bytes(key,encoding='utf-8'),
    bytes(msg,encoding='utf-8'),
    digestmod=hashlib.sha256).hexdigest()
    return signature


def checkout(request):
    # data = request.user.Order.objects.all()
    id = "rzp_test_wiAaeKveL6fg77"
    key = "thfUqxKGoWOoFDtOQWoteIgc"
     
    client = razorpay.Client(auth=(id,key))
    client.set_app_details({"title" : "Django", "version" : "4.0.3"})
    DATA = {
        "amount": 100,
        "currency": "INR",
        "receipt": "recieptidisastring",
        "notes":{
            "note1":"no-note"
        }
    }
    thisorder = client.order.create(data=DATA)
    #order_id = client.order.all()['items'][-1]['id']
    order_data = {
        "data":DATA,
        "order_id":thisorder['id'],
        "callback_url":'status/'
    }
    
    return render(request,'payments/checkout.html',{'order_data':order_data})

@csrf_exempt
def paymenthandler(request):
    id = "rzp_test_wiAaeKveL6fg77"
    key = "thfUqxKGoWOoFDtOQWoteIgc"
    
    if request.method=="POST":
        
        client = razorpay.Client(auth=(id,key))
        created_order_id = client.order.all()['items'][0]['id']
        # response order_id:
        returned_order_id = request.POST['razorpay_order_id']

        assert created_order_id==returned_order_id, "created order_id != returned order_id"

        try:

            response_params={
                'razorpay_order_id':created_order_id,
                'razorpay_payment_id':request.POST['razorpay_payment_id'],
                'razorpay_signature':request.POST['razorpay_signature']
            }
        except KeyError:
            raise "No such values in request.POST"
        

        generated_signature = generate_signature(created_order_id,
        response_params['razorpay_payment_id'],key)
        
        # result = hmac.compare_digest(generated_signature,response_params['razorpay_signature'])
        # result = client.utility.verify_payment_signature(response_params)
        assert generated_signature==response_params['razorpay_signature'], \
        "type mismatch or value not equal b/w generated_signature and returned signature"
        
        if client.payment.fetch(response_params['razorpay_payment_id'])['status']=='captured':
            print('captured')
            return redirect(success,permanent=True)
        
        elif client.payment.fetch(response_params['razorpay_payment_id'])['status']=='failed':
            return redirect(failure,permanent=True)

    else:
        return HttpResponseBadRequest()

def success(request):
    msg="Payment Successfully Captured."
    return render(request,'payments/success.html',{"msg":msg})

def failure(request):
    return render(request,'payments/failure.html',{"msg":"Failed: Could not Capture the Payment"})