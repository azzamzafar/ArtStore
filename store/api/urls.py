from django.urls import path
from store.api.views import product_list,product_detail,generate_tokens

urlpatterns = [
    path("generate_token/",generate_tokens,name="api_tokens"),
    path("products/",product_list,name="api_product_list"),
    path("products/<int:pk>/",product_detail,name="api_product_detail"),
]