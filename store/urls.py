from django.urls import path
from store.views import ProductListView, ProductDetailView,cartview, orderview
urlpatterns = [
    path('',ProductListView.as_view(),name='home'),
    path("<int:pk>/",ProductDetailView.as_view(),name='Product-detail'),
    path('cart/',cartview,name='cart'),
    path('order-summary/',orderview,name='order-summary')
]