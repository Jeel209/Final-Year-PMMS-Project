#!/usr/bin/env python
# coding: utf-8
go to sandbox.paypal.com
sign up and select business account

go to developer.paypal.com
sign up and make a business account
give all the details what it asks

all the payment notification will come in developer account
    #Install django-paypal

pip install django-paypal


#add 'paypal.standard.ipn' Installed apps in settings.py

python manage.py migrate# add this 2 line in settings.py

PAYPAL_RECEIVER_EMAIL = 'youremail@gmail.com'

PAYPAL_TEST = True

# add url in main application's urls.py
path('paypal/', include('paypal.standard.ipn.urls')),In cart/views.py

def process_payment(request):
    pass

In cart/urls.py
from .views import process_payment
path('process_payment/',process_payment,name='process_payment')In cart.html

<div>
    <a href="#" class="btn btn-success btn-block btn-sm" style="margin-top: 10px">
        Proceed to Pay <span id="btamt"></span>
    </a>
</div>
add code in cart/views.py

from django.shortcuts import reverse
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm

def process_payment(request):
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '100'
        'item_name': 'abcd',
        'invoice': 1,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format('127.0.0.1:8000',
                                           reverse('paypal-ipn')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'ecommerce_app/process_payment.html', {'form': form})Make process_payment.htmlTO render the paypal redirecting form 

add 

<div class="conainer-fluid" >
		<div class="row">
			<div class="col-md-12 mx-auto my-5 p-5 text-center" style="margin-top: 100px;margin-bottom: 100px"> 
				{{form.render}}
			</div>
			
		</div>
	</div>

between

{% block content %}

{% endblock %}Now we need to fetch cart detailsUpdate process_payment function

import random
from django.http import HttpResponse

def process_payment(request):
    items = Cart.objects.filter(user_id__id=request.user.id,status=False)
    product = ""
    amt = 0
    inv = "INV-"+str(random.randint(1,1000000))   # for unique invoice id
    cart_ids = ""
    p_ids = ""
    for i in items:
        product += str(i.products.name)+"\n"
        p_ids += str(i.products.id)+","
        amt += float(i.products.price)
        inv += str(i.id)
        cart_ids += str(i.id)+","
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '100',
        'item_name': 'abcd',
        'invoice': 1,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format('127.0.0.1:8000',
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('Home:Products:Cart:payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('Home:Products:Cart:payment_canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'cart_temp/process_payment.html', {'form': form})



Make payment_done.html and payment canceled.html


Make views for payment done and payment canceled

def payment_done(request):
    return HttpResponse("Payment done")


def payment_canceled(request):
    return HttpResponse('payment canceled')


make urls for payment done and payment canceled

path('payment_done/',payment_done,name='payment_done')
path('payment_canceled/',payment_canceled,name='payment_canceled'),







Make order model in models.py

class Order(models.Model):
	cust_id = models.ForeignKey(User,on_delete=models.CASCADE)
	cart_ids=models.CharField(max_length=250)
	product_ids=models.CharField(max_length=250)
	invoice_id=models.CharField(max_length=250)
	status=models.BooleanField(default=False)
	processed_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.cust_id.username
        

In admin.py

admin.site.register(Order)


In views.py

  in process_payments
    usr = User.objects.get(username=request.user.username)
    ord = Order(cust_id=usr,cart_ids=cart_ids,product_ids=p_ids)
    ord.save()
    ord.invoice_id = str(ord.id)+inv
    ord.save()
    request.session['order_id'] = ord.id
    
    

To make good payment done and payment fail page 
    use  check and cross images
    
    
Make payment_success.html and payment_failed.html 

Payment_success.html

    {% extends 'common.html' %}
    {% load static %}

    {% block content %}	

        <section class="contact-img-area">
                <div class="container">
                    <div class="row">
                        <div class="col-md-12 text-center">
                            <div class="con-text">
                                <h2 class="page-title">Payment</h2>
                                <p><a href="#">Payment</a> | Success</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        <div class="conainer-fluid" >
            <div class="row" style="margin-top: 120px;">
                <div class="col-md-3"></div>
                    <div class="col-md-6 mx-auto my-2 text-center" style="margin-top: 100px;margin-bottom: 100px; box-shadow:                       0px 0px 10px grey"> 
                    <img src="{% static 'images/success.gif' %}" height="200" width="200">
                    <br>
                    <h1 class="alert alert-success">Payment Successfull</h1>
                    <div class='my-3'>
                        <a href="{% url 'Home:Products:shop' %}" class="btn btn-success" style="margin-bottom: 50px">Continue                           Shopping</a>
                    </div>
                </div>
                <div class="col-md-3"></div>
            </div>
        </div>

    {% endblock %}


Payment_failed.html

    {% extends 'common.html' %}
    {% load static %}

    {% block content %}	
        <section class="contact-img-area">
                <div class="container">
                    <div class="row">
                        <div class="col-md-12 text-center">
                            <div class="con-text">
                                <h2 class="page-title">Payment</h2>
                                <p><a href="#">Payment</a> | Failed</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        <div class="conainer-fluid" >
            <div class="row" style="margin-bottom: 50px">
                <div class="col-md-3"></div>
                <div class="col-md-6 mx-auto text-center" style="margin-top: 100px;margin-bottom: 100px; box-shadow: 0px 0px                   10px grey"> 
                    <img src="{% static 'images/failed.jpg' %}" height="400" width="400">
                    <br>
                    <h1 class="alert alert-failed">Payment Failed</h1>
                    <div class='my-3'>
                        <a href="{% url 'Home:Products:shop' %}" class="btn btn-success" style="margin-bottom: 50px">Continue                            Shopping</a>
                        <a href="{% url 'Home:Products:Cart:add_to_cart' %}" class="btn btn-primary" style="margin-bottom:                             50px">Go to Cart</a>
                    </div>
                </div>
                <div class="col-md-3"></div>

            </div>
        </div>

    {% endblock %}
In views.py
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_done(request):
    template = 'cart_temp/payment_success.html'
    return render(request,template)


@csrf_exempt
def payment_canceled(request):
    template = 'cart_temp/payment_failed.html'
    return render(request,template)
    
    
    
After payment success we need to make order and cart status True
    
def payment_done(request):
    if 'order_id' in request.session:
        order_id = request.session["order_id"]
        order_obj = get_object_or_404(Order,id=order_id)
        order_obj.status = True
        order_obj.save()

        for i in order_obj.cart_ids.split(",")[:-1]:
            cart_object = Cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()
    template = 'cart_temp/payment_success.html'
    return render(request,template)