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

from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
import debug_toolbar

from comparator.views import home_view, add_product, show_gpu_view, show_cpu_view, show_ram_view, show_product_view, search_view, observe_view, user_observed_view
from accounts.views import register_view

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('compare-products/show-gpu', show_gpu_view, name="show-gpu"),
    path('compare-products/show-cpu', show_cpu_view, name="show-cpu"),
    path('compare-products/show-ram', show_ram_view, name="show-ram"),
    path('compare-products/<int:num>', show_product_view, name="show-specific"),
    path('search-result/', search_view, name="search"),
    path('compare-products/<int:num>/observe', observe_view, name="observe"),
    path('observed', user_observed_view, name="user-observed"),

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

    path('product/add', add_product, name='add_product'),
    
]

urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
