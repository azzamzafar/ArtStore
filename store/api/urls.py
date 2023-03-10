from django.urls import path
from store.api.product_views import product_list,product_detail,generate_tokens,product_stats
from store.api.order_views import myorders,user_orders
from store.api.cart_views import mycart,user_carts
urlpatterns = [
    path("generate_token/",generate_tokens,name="api_tokens"),
    path("products/",product_list,name="api_product_list"),
    path("products/<int:pk>/",product_detail,name="api_product_detail"),
    path("products/stats/<int:pk>/",product_stats,name="api_prod_stats"),
    #invoice paths
    path("get_my_orders/",myorders,name='myorders'),
    path("get_user_orders/",user_orders,name='user_orders'),
    #cart paths
    path("get_my_cart/",mycart,name='mycart'),
    path("get_user_carts/",user_carts,name='user_carts')
]