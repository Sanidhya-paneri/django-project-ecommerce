from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Home"),
    path('login/', views.handleLogin, name="login"),
    path('signup/', views.handleSignup, name="signup"),
    path('product/<int:id>', views.products, name="Products"),
    path('logout/', views.handleLogout, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('updateitem/', views.updateitems, name="updateitem"),
    path('checkout/', views.checkout, name="checkout"),
    path('process_order/', views.processorder, name="processorder"),

]
