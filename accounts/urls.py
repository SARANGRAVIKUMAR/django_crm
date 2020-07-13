from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerPage,name="register"),
    path('login/', views.loginPage, name="login"),
    path('logoutUser/', views.logoutUser, name="logout"),
    path('', views.Home, name="home"),
    path('products/', views.Products, name="products"),
    path('customer/<int:pk>/', views.Customer, name="customer"),
    path('create_order/', views.create_Order, name="create_order"),
    path('update_order/<int:id>/', views.update_order, name="update_order"),
    path('delete/<int:id>/', views.delete, name="delete"),
]
