from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.db.models import Min, Max
from django.conf import settings

from django.views.generic import TemplateView, View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from liqpay.liqpay3 import LiqPay
from datetime import datetime
import json

from .models import *
from .utils import *
from .forms import *

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0]
        if group == '':
            return redirect('store')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func

def adminpanel(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0]
        if group:
            shippings = ShippingAddress.objects.all()
            for shipping in shippings:
                orderitems = OrderItem.objects.get(order__id=shipping.order.id)
            context = {
                'shippings': shippings,
                'orderitems': orderitems,
            }
            return render(request, 'store/admin.html', context)

def category(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    categories = Category.objects.all()

    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/category.html', context)

def subcategory(request, category_id):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    category = Category.objects.get(id=category_id)
    subcategories = MinCategory.objects.filter(category__id=category_id)

    context = {
        'category': category,
        'subcategories': subcategories,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/subcategory.html', context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/checkout.html', context)

def searchCategory(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if request.method == 'POST':
        category = request.POST.get('search_form')
        if category:
            search_item = Category.objects.filter(name__icontains=category)
            context = {
                'items': items,
                'order': order,
                'cartItems': cartItems,
                'search_item': search_item,
            }
            return render(request, 'store/search.html', context)
        else:
            categories = Category.objects.all()

            context = {
                'categories': categories,
                'items': items,
                'order': order,
                'cartItems': cartItems,
            }
            return render(request, 'store/category.html', context)

class PayView(TemplateView):
    template_name = 'store/pay.html'

    def get(self, request, *args, **kwargs):
        """ My Data """
        data = cartData(request)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        transaction_id = datetime.now().timestamp()

        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': float(order['get_cart_total']),
            'currency': 'UAH',
            'description': 'Количество товаров: ' + str(order['get_cart_items']),
            'order_id': 'order_id_'+ str(transaction_id),
            'version': '3',
            'sandbox': 0, # sandbox mode, set to 1 to enable it
            'server_url': 'https://test.com/billing/pay-callback/', # url to callback view
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})

    @method_decorator(csrf_exempt, name='dispatch')
    class PayCallbackView(View):
        def post(self, request, *args, **kwargs):
            liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
            data = request.POST.get('data')
            signature = request.POST.get('signature')
            sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
            if sign == signature:
                print('callback is valid')
            response = liqpay.decode_data_from_str(data)
            print('callback data', response)
            return HttpResponse()

def products(request, subcategory_id):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    subcategory = MinCategory.objects.get(id=subcategory_id)
    products = Product.objects.filter(subcategory__id=subcategory_id)
    minimal_cost = Product.objects.all().aggregate(Min('price'))
    maximum_cost = Product.objects.all().aggregate(Max('price'))

    context = {
        'subcategory': subcategory,
        'products': products,
        'minimal_cost': minimal_cost['price__min'],
        'maximum_cost': maximum_cost['price__max'],
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/products.html', context)

def current_product(request, subcategory_id, product_id):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    current_product = Product.objects.get(subcategory__id=subcategory_id, id=product_id)

    context = {
        'current_product': current_product,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/current_product.html', context)

def contact_info(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
    }
    return render(request, 'store/contact.html', context)

def delivery_info(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
    }
    return render(request, 'store/delivery.html', context)

def oplata_info(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
    }
    return render(request, 'store/oplata.html', context)

def feedback_info(request):
    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        contact_form = ContactUsForm(request.POST)
        if contact_form.is_valid():
            MailBox.objects.create(name=request.POST['name'], body=request.POST['message'],
                email=request.POST['email'])

    context = {
        'cartItems': cartItems,
    }
    return render(request, 'store/feedback.html', context)

def updateItem(request):
    data = json.load(request)

    productId = data['productId']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1

    if action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    print(data)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True

    order.save()

    print(order)

    orderitem = OrderItem.objects.get(id=order.id)

    if order.shipping:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            phone = data['shipping']['telephone'],
            orderitems = orderitem,
        )

    return JsonResponse('Payment complet!', safe=False)