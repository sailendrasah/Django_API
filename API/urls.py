"""
URL configuration for API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from .views import get_user, user_registration, login, verify_otp, update_user,froget_password,rest_paswword,delete
from .swagger_docs import openapi_json, swagger_ui

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', swagger_ui, name='swagger-ui'),
    path('openapi.json', openapi_json, name='openapi-schema'),
    path('register/', user_registration,name="user_registration"),
    path('login/', login,name="login"),
    path('verify_otp/', verify_otp,name="verify_otp"),
    path('get_user/', get_user, name="get_user"),
    path('update_user/', update_user, name="update_user"),
    path('froget_password/', froget_password, name="froget_password"),
    path('rest_paswword/', rest_paswword, name="rest_paswword"),
    path('delete/', delete, name="delete"),
]
