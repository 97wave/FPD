"""orders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

from backend.views import LoginView, SignUp, PermissionUp
# PartnerUpdate, RegisterAccount,  CategoryView, ShopView,\
#     ProductInfoView, BasketView, AccountDetails, ContactView, OrderView, PartnerState, \
#     PartnerOrders, ConfirmAccount


app_name = 'backend'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='log_in'),
    path('signup/', SignUp.as_view(), name='sign_up'),
    path('permission_up/', PermissionUp.as_view(), name='permission_up'),
]
