from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
import json


def index(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        items = order.orderitem_set.all()
        orderItems = order.get_total_item

    else:
        items = []
        orderItems = 0

    product = Product.objects.all()

    params = {'product':product, 'orderItems':orderItems}
    return render(request, 'store/index.html', params)

def products(request, id):
    product = Product.objects.filter(id=id)

    return render(request, 'store/product.html', {'product':product[0]})

def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            return redirect('/store/')
        else:
            messages.error(request, "Wrong Credentials")
            return redirect('/store/')

    else:
        return HttpResponse("not found")

def handleSignup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #Checks
        if password != password2:
            messages.error(request, "Passwords don't match!")
            return redirect('/store/signup')

        #data to databse
        puser = User.objects.create_user(username, email, password)
        puser.save()
        messages.success(request, "Signup succesfull")
        return redirect('/store/')
    else:
        return HttpResponse("not found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Succesfully logout!")
    return redirect('/store/')

    return HttpResponse('error')

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        items = order.orderitem_set.all()
        orderItems = order.get_total_item
    else:
        items = []
    params = {'items':items, 'order':order, 'orderItems': orderItems}
    return render(request, 'store/cart.html', params)

def updateitems(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(productId)
    print(action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        print('added')
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('items updated', safe=False)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        items = order.orderitem_set.all()
        orderItems = order.get_total_item
    else:
        items = []
    params = {'items':items, 'order':order, 'orderItems': orderItems}

    return render(request, 'store/checkout.html', params)

def processorder(request):
    return JsonResponse('payment complete', safe=False)









    #'''allproducts = []
    #product_cats = Product.object.values('category', 'id')
    #cats = {item['category'] for item in product_cats}
    #for cat in cats:
    #product = Product.object.filter(category=cat)'''