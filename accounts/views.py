from django.shortcuts import render, redirect
from .decorators import unauthenticated_user
from .models import Order, coustomer, Product
from .forms import OrderForm, createUserForm
from .filter import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "username or password is incorrect")

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def registerPage(request):
    form = createUserForm()
    if request.method == "POST":
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created Successfully for " + user)
            return redirect('login')

        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)


@login_required(login_url="login")
def Home(request):
    orders = Order.objects.all()
    customer = coustomer.objects.all()
    total_customers = customer.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customer,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url="login")
def Products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url="login")
def Customer(request, pk):
    customer = coustomer.objects.get(id=pk)
    orders = customer.order_set.all()  # quering customer child fields from the model
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter,
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url="login")
def create_Order(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def update_order(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def delete(request, id):
    order = Order.objects.get(id=id)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {
        'order': order,
    }
    return render(request, 'accounts/delete.html', context)
