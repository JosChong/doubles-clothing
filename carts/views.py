from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic.edit import FormMixin

from products.models import ProductSizeVariation
from .models import Cart, CartItem
from orders.models import UserCheckout, Order, UserAddress
from orders.forms import GuestCheckoutForm

from orders.mixins import CartOrderMixin

from django.conf import settings
from django.contrib import messages
import braintree

# Create your views here.


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "carts/cart_view.html"

    def get_object(self, *args, **kwargs):
        # This will end the session when the user closes their browser.
        self.request.session.set_expiry(0)
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart.id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get("item")
        # Default for deleted items will be set to False.
        delete_item = request.GET.get("delete", False)
        item_added = False  # Default for added items
        if item_id:
            item_instance = get_object_or_404(ProductSizeVariation, id=item_id)
            # Giving the quantity a default value of 1
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            # We will either have a created item, or an item that is already in the cart
            cart_item, created_item = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            if created_item:
                item_added = True  # If a new item is added to the cart it will return as True
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart_view"))
        if request.is_ajax():  # If an AJAX call happens then...
            # Then print out what the request gives back
            print(request.GET.get("item"))
            try:
                item_total = cart_item.item_total
            except:
                item_total = None
            try:
                subtotal = cart_item.cart_subtotal
            except:
                subtotal = None
            data = {
                "deleted": delete_item,
                "created": item_added,
                "item_total": item_total,
                "subtotal": subtotal,
                # "cart_total": cart_total,
                # "tax_total": tax_total,
                # "total_items": total_items,
            }
            return JsonResponse(data)  # Return a JSON Response.
        context = {
            "object": self.get_object()
        }
        print(context)
        template = self.template_name
        return render(request, template, context)


class CheckoutView(CartOrderMixin,FormMixin, DetailView):
    model = Cart
    template_name = "carts/checkout_view.html"
    form_class = GuestCheckoutForm

    def get_order(self, *args, **kwargs):
        cart = self.get_object()
        new_order_id = self.request.session.get("order_id")
        if new_order_id is None:
            new_order = Order.objects.create(cart=cart)
            self.request.session["order_id"] = new_order.id
        else:
            new_order = Order.objects.get(id=new_order_id)
        return new_order

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart == None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        user_checkout_id = self.request.session.get("user_checkout_id")
        # or if request.user.is_guest:
        if not self.request.user.is_authenticated() or user_checkout_id == None:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
        elif self.request.user.is_authenticated() or user_checkout_id != None:
            user_can_continue = True
            # return redirect("address_select_form_view")
        else:
            pass
        if self.request.user.is_authenticated():
            user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
            user_checkout.user = self.request.user
            user_checkout.save()
            context["client_token"] = user_checkout.get_client_token()
            self.request.session["user_checkout_id"] = user_checkout.id

        elif not self.request.user.is_authenticated() and user_checkout_id == None:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
        else:
            pass
        if user_checkout_id != None:
            user_can_continue = True
            if not self.request.user.is_authenticated():
                user_checkout_check = UserCheckout.objects.get(id = user_checkout_id)
                context["client_token"] = user_checkout_check.get_client_token()
        # This will allow use to show the order in the html.
        context["order"] = self.get_order()
        context["user_can_continue"] = user_can_continue
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user_checkout, created = UserCheckout.objects.get_or_create(email=email)
            request.session["user_checkout_id"] = user_checkout.id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("checkout_view")

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        if cart == None:
            return redirect("cart_view")
        new_order = self.get_order()
        user_checkout_id = request.session.get("user_checkout_id")
        if user_checkout_id != None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            if new_order.billing_address == None or new_order.shipping_address == None:
                return redirect("address_select_form_view")
            new_order.user = user_checkout
            new_order.save()
        return get_data


class CompleteCheckoutView(CartOrderMixin,View):
    def post(self,request,*args,**kwargs):
        print(request.POST)
        order = self.get_order()
        order_total = order.order_total
        nonce = request.POST.get('payment_method_nonce')
        if nonce:
            result = braintree.Transaction.sale({
                "amount": order_total,
                "payment_method_nonce": nonce,
                "billing": {"postal_code": "%s" % (order.billing_address.zipcode)},
                "options": {"submit_for_settlement": True}
                })
            if result.is_success:
                # result.transaction.id to order
                print(result.transaction.id)
                order.mark_completed(order_id=result.transaction.id)
                messages.success(request,"Thank you for your order.")
                del request.session["cart_id"]
                del request.session["order_id"]
            else:
                messages.success(request,"%s" %(result.message))
                return redirect("checkout_view")
            return redirect("order_detail_view", pk=order.pk)

    def get(self,request,*args,**kwargs):
        """This GET call will redirect us back to the checkout URL
        otherwise we would raise a 405 Forbidden Error"""
        return redirect("checkout_view")
