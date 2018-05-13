"""doubles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from products import views
from carts.views import CartView, CheckoutView, CompleteCheckoutView
from orders.views import AddressSelectFormView, AddressCreateFormView, OrderListView, OrderDetailView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^$', views.splash_view, name = 'splash_view'),
    url(r'^browse$', views.ProductListView.as_view(), name = 'list_view'),
    url(r'^view/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name = 'detail_view'),

    url(r'^browse/mens$', views.MensListView.as_view(), name = 'mens_list_view'),
    url(r'^browse/womens$', views.WomensListView.as_view(), name = 'womens_list_view'),
    url(r'^browse/shoes$', views.ShoesListView.as_view(), name = 'shoes_list_view'),
    url(r'^browse/accessories$', views.AccessoriesListView.as_view(), name = 'accessories_list_view'),
    url(r'^browse/collections$', views.CollectionsListView.as_view(), name = 'collections_list_view'),

    url(r'^orders/$', OrderListView.as_view(), name = "order_list_view"),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetailView.as_view(), name = "order_detail_view"),
    url(r'^cart/$', CartView.as_view(), name="cart_view"),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout_view'),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name="address_select_form_view"),
    url(r'^checkout/address/add$', AddressCreateFormView.as_view(), name="address_create_form_view"),
    url(r'^checkout/confirm/$', CompleteCheckoutView.as_view(),name="complete_checkout_view"),

    url(r'^browse/sort$', views.sort_list_view, name = 'sort_list_view'),

    url(r'^about$', views.unavailable_view, name = 'unavailable_view'),
    url(r'^contact$', views.unavailable_view, name = 'unavailable_view'),
    url(r'^locations$', views.unavailable_view, name = 'unavailable_view'),
    url(r'^shipping$', views.unavailable_view, name = 'unavailable_view'),
    url(r'^faq$', views.unavailable_view, name = 'unavailable_view'),
    url(r'^terms$', views.unavailable_view, name = 'unavailable_view')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
