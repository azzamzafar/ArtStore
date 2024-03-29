"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django_registration.backends.activation.views import RegistrationView
from customers_auth.forms import ProfileForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payments/', include('payments.urls')),
    path('accounts/register/',RegistrationView.as_view(form_class=ProfileForm)
    ,name='django_registration_register'),
    path('accounts/',include('django_registration.backends.activation.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/profile/',include('customers_auth.urls')),
    path('',include('store.urls')),
    path("api/v1/",include("store.api.urls")),
    
]
urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)