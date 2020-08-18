from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from.forms import OrderForm
from .models import *
# Create your views here.
def home(request):

    orders = Order.objects.all()
    customers = Customer.objects.all()

    # totalCustomers = customers.count()
    totalOrders = orders.count()

    orders_delivered = orders.filter(status = 'Delivered').count()
    orders_pending = orders.filter(status = 'Pending').count()

    context ={
        'orders':orders,
        'customers':customers,
        'total_orders': totalOrders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending
    }
    return render(request,'accounts/dashboard.html',context)

def product(request):
    products = Product.objects.all()
    return render(request,"accounts/products.html",{'products':products})

def customers(request,pk):
    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()
    context = {
        'customer':customer,
        'orders':orders,
        'total_orders':orders.count()
    }
    return render(request,"accounts/customers.html",context)

def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset = Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method=="POST":
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context ={'formset':formset}
    return render(request,'accounts/order_form.html',context)

def updateOrder(request,pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)

    if request.method=="POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context ={'form':form}
    return render(request,'accounts/order_form.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get(id = pk)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request,'accounts/delete.html',context)