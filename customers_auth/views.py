from django.shortcuts import render,redirect
from customers_auth.forms import ContactForm
from customers_auth.models import Customer
# Create your views here.
def profile(request):
    if request.user.is_authenticated:
        return render(request,"customers_auth/profile.html")
    
def update_profile(request):
    
    if request.user.is_authenticated:
    
        if request.method=="POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                phone = form.cleaned_data['phone']
                country = form.cleaned_data['country']
                state = form.cleaned_data['state']
                city = form.cleaned_data['city']
                address1 = form.cleaned_data['address1']
                address2 = form.cleaned_data['address2'] 
                
                Customer.objects.filter(email=request.user.email).update(phone=phone,country=country,state=state,city=city,address1=address1,address2=address2) 
                
                return redirect('http://127.0.0.1:8000/accounts/profile/',permanent=True)
        else:
            form = ContactForm()
    else:
        form = None
    return render(request,"customers_auth/update_profile.html",{"form":form})