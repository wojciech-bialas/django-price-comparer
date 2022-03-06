"""djangoapp URL Configuration

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
from django.urls import path, include

from comparator.views import home_view, add_product
from accounts.views import register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('compare/add', home_view, name="add-comparison"),
    path('compare/show', home_view, name="show-comparisons"),

    # accounts/login/ [name='login']
    # accounts/logout/ [name='logout']
    # accounts/password_change/ [name='password_change']
    # accounts/password_change/done/ [name='password_change_done']
    # accounts/password_reset/ [name='password_reset']
    # accounts/password_reset/done/ [name='password_reset_done']
    # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/reset/done/ [name='password_reset_complete']
    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/register', register_view, name='register'),
    path('product/add', add_product, name='add_product')
]
