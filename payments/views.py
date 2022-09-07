from ast import Or
from typing import OrderedDict
from django.db import DatabaseError
from django.http import HttpResponseBadRequest
from django.shortcuts import render,redirect
import razorpay
from django.views.decorators.csrf import csrf_exempt
from .forms import SignatureVerificationForm as svf
import hmac,hashlib
# Create your views here.

def generate_signature(order_id,payment_id,key):
    msg = order_id+"|"+payment_id

    signature = hmac.new(bytes(key,encoding='ascii'),bytes(msg,encoding='ascii'),digestmod=hashlib.sha256).hexdigest().upper()
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
        order_id,payment_id,signature=None,None,None

        try:

           
            order_id = request.POST.get('razorpay_order_id','')
            payment_id = request.POST.get('razorpay_payment_id','')
            signature = request.POST.get('razorpay_signature','')
            print(request.POST)
            print(f'{order_id}{type(order_id)}{type(payment_id)}{payment_id}{signature}{type(signature)}')
        except KeyError:
            return HttpResponseBadRequest()
        #if form.is_valid():
        

        client = razorpay.Client(auth=(id,key))
        created_order_id = client.order.all()['items'][-1]['id']
        print(created_order_id==order_id[0])
        print(type('created_order_id'))
        response_param ={
            'razorpay_order_id':order_id,
            'razorpay_payment_id':payment_id,
            'razorpay_signature':signature
        }
        #generated_signature = generate_signature(created_order_id,payment_id,key)
        result = client.utility.verify_payment_signature(response_param)
        if  result is None:
            try:
                if client.payments.fetch(payment_id)['status']=='captured':
                    print('captured')
                    return redirect(success,permanent=True)
                
            except:
                return redirect(failure,permanent=True) 
        else:
            return redirect(failure,permanent=True)       
    else:
        return HttpResponseBadRequest()

def success(request):
    return render(request,'orders/track.html')

def failure(request):
    return render(request,'payments/failure.html')