#!/usr/bin/env python
# coding: utf-8

# <h3>Create an app named cart and Register it in settings.py</h3>

# <h3>In models.py </h3>
# <pre>
# from django.contrib.auth.models import User
# from products.models import Product
# from django.core.validators import MinValueValidator
# 
# class Cart(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     products = models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)
#     status = models.BooleanField(default=False)
#     added_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
# 
#     def __str__(self):
#         return self.user.username + '-' + self.products.name
# </pre>
# 
# 
# <pre>python manage.py makemigrations
# pyrhon manage.py migrate</pre>
# 
# 
# <h3>Register app in admin.py</h3>
# <pre>from .models import Cart
# admin.site.register(Cart)</pre>
# 
# 
# Make cart_temp folder in Templates Folder

# <h4>Make cart.html, make its view and url</h4>
# <h4>In cart.html</h4>
# 
# <pre>
# Use wishlist.html from template for making cart page in cart_temp folder which is available in Templates Folder
# remove unnecessary table items
# Do some customisation
# remove Add To Cart button etc...
# only 1 item should be in table
# 
# <h4>In views.py</h4>
# 
# def add_to_cart(request):
#     template = 'cart_temp/cart.html'
#     return render(request,template)
# 
# <h4>In urls.py</h4>
# from .views import add_to_cart
# 
# app_name = 'Cart'    
# 
# path('cart/',add_to_cart,name='add_to_cart')
# 
# 
# </pre>

# <h4>Make Add to Cart button in Shop page</h4>

<pre>
<form action="{% url 'Home:Products:Cart:add_to_cart' %}" method="post">{% csrf_token %}
    <button type="submit" class="btn btn-success">
        <i class="fa fa-shopping-cart"></i> 
        Add To Cart
    </button>
</form>
</pre>
# <pre>
# user must be authenticated to access the cart
# 
# In views.py
# 
# from django.contrib.auth.decorators import login_required
# 
# @login_required
# def ad_to_cart(request):
#     ...
#     ...
#     
#     
# </pre>
<h3>Now when we click on add to cart button on shop page, that particular item need to be added in cart</h3>
<pre>
in shop.html

in form part of add to cart button
add

<input type="hidden" name="pid" value="{{ product.id }}">
<input type="hidden" name="qty" value="1">


in views.py

update add_to_cart view

from django.shortcuts import get_object_or_404
from .models import Cart
from django.contrib import messages 
from django.contrib.auth.models import User
from products.models import Product

@login_required
def add_to_cart(request):
    items = Cart.objects.filter(user__id=request.user.id,status=False)
    context = {}
    context['items'] = items
    if request.user.is_authenticated:    
        if request.method == 'POST':
            pid = request.POST["pid"]
            qty = request.POST["qty"]
            is_exist = Cart.objects.filter(products__id=pid,user__id=request.user.id,status=False)
            if len(is_exist)>0:
                messages.error(request,'Item already exist in Cart')
            else:
                product = get_object_or_404(Product,id=pid)
                user = get_object_or_404(User,id=request.user.id)
                c = Cart(user=user,products=product,quantity=qty)
                c.save()
                messages.success(request,'{} Added in your Cart'.format(product.name))
    else:
        context['status'] = 'Please login to view your cart'
    return render(request, 'cart_temp/cart.html',context)






in cart.html


add for loop using items key(context) from views.py
{% for item in items %}
    ...
    ...
{% endfor %}



</pre>
<pre>
In cart.html

we need to add django variables and urls

name = {{item.products.name}}
image_url = {% url 'Home:Products:singleproduct' item.products.id %}
price = {{item.products.price}}


<h3>Now on clicking add to cart button product will be added to cart<h3>

</pre><h3> operation on cart data e.g. grand Total, handling quantity etc. </h3>



<pre>
In views.py

def get_cart_data(request):
    pass

In urls.py

from .views import get_cart_data
path('get_cart_data/',get_cart_data,name='get_cart_data')


In cart.html

<script>
    function grandTotal(){
        $.ajax({
            url:"{% url 'Home:Products:Cart:get_cart_data' %}",
            type:'get',
            success:function(data){
                alert(data)
                }
            })
        }grandTotal()
</script>



update get_cart_data view

from django.http import JsonResponse

def get_cart_data(request):
    items = Cart.objects.filter(user__id=request.user.id,status=False)
    total,quantity = 0,0
    for i in items:
        total += i.products.price * i.quantity
        quantity += i.quantity
    
    res = {'total':total,'quan':quantity}
    return JsonResponse(res) 



<h3>Now check by in browser that by calling get_cart_data page, it is working or not, and check on cart page there is an alert or not</h3>

</pre><pre>
<h3> Now make html table for display grand total and quantity on cart page. </h3>

<tr>
    <td class="cen">
        <span class="wishlist-in-stock">Total</span>
    </td>
    <td class="sop-cart an-sh">
        <div class="tb-beg">
            <a href="#"></a>
        </div>
        <div class="last-cart ">
            <a class="" href=""></a>
        </div>
    </td>
    <td class="sop-cart">
        <div class="tb-product-price font-noraure-3">
            <span class="amount"></span>
        </div>
    </td>
    <td class="sop-cart" id="quantity">
        <div class="tb-product-price font-noraure-3">
            <span class="amount"></span>
        </div>
    </td>
    <td class="cen" id="item_total">
    </td>
    <td class="cen">
        <span class="wishlist-in-stock"></span>
    </td>
    <td class="sop-icon1">
        <a href="#">
            <i class=""></i>
        </a>
    </td>
</tr>    



<script>
            function grandTotal(){
                $.ajax({
                    url:"{% url 'Home:Products:Cart:get_cart_data' %}",
                    type:'get',
                    success:function(data){
                        $("#item_total").html("&#8377;"+data.total)
                        $("#quantity").html(data.quan)
                    }
                })
            }grandTotal()
        </script>


<h4>Handling Quantity</h4>

we need plus and minus icon to increase and decrease quntity

In cart.html

In quantity <td>
<td>
<div class="tb-product-price font-noraure-3">
    <div class="col-md-3"></div>
    <div class="col-md-1"> 
        <a href=""  onclick="change_quan('{{item.id}}','plus')">
            <i class="fa fa-plus" style="margin-top: 12px;" ></i>
        </a>
    </div>
    <div class="col-md-4">
        <input class="form-control" type="number" name="" value="{{item.quantity}}" id= "cart{{item.id}}">
    </div>
    <div class="col-md-1" style="margin-left: -12px;margin-top: 10px;">
        <a href="" onclick="change_quan('{{item.id}}','minus')">
            <i class="fa fa-minus p-5 rounded-circle"  ></i>
        </a>
    </div>
</div>
</td>



In cart.html

function change_quan(id,action){
                alert(id)
                alert(action)
            }

Check in cart page alert is there or not while clicking plus or minus in quantity

function change_quan(id,action){
                let old = $("#cart"+id).val();
                
                quan=0
                if(action=="plus"){
                    quan += parseInt(old)+1
                }else{
                    quan += parseInt(old)-1 
                } 

                $("#cart"+id).val(quan)  # updates quantity on cart page not in database
            }


<h4>We need to update quantity in database also</h4>

In views.py

def change_quan(request):
    pass
    
In urls.py

path('change_quan/',change_quan,name='change_quan')



In cart.html

function change_quan(id,action){
    let old = $("#cart"+id).val();
                
    quan=0
    if(action=="plus"){
        quan += parseInt(old)+1
    }else{
        quan += parseInt(old)-1 
    } 

    $("#cart"+id).val(quan)  

    $.ajax({
        url:"{% url 'Home:Products:Cart:change_quan' %}",
        type:"get",
        data:{cid:id,quantity:quan},
        success:function(data){
            grandTotal();
        }
    })
}







Remove from cart

In cart.html

give it to cross icon

<td class="sop-icon1">
    <a href="" onclick="remove_cart('{{item.id}}')">
        <i class="fa fa-times"></i>
    </a>
</td>

function remove_cart(id){
    $.ajax({
        url:"{% url 'Home:Products:Cart:change_quan' %}",
        data:{delete_cart:id},
        success:function(data){
            grandTotal();
        }
    })
}



In views.py

def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]   # cid is cart id
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(Cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)
    
    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(Cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)



</pre>
