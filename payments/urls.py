from django.urls import path
from . import views
urlpatterns = [
    path('checkout',views.checkout,name='checkout'),
    path('status/',views.paymenthandler,name='status'),
    path('failure/',views.failure,name='failure'),
    path('success/',views.success,name='success')
]