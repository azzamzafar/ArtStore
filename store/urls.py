from django.urls import path
from store.views import ProductListView, ProductDetailView, cart_order,cartview
urlpatterns = [
    path('',ProductListView.as_view(),name='home'),
    path("<int:pk>/",ProductDetailView.as_view(),name='Product-detail'),
    path('cart/',cartview,name='cart'),
    path('cart/order/',cart_order,name='cart-order')
]