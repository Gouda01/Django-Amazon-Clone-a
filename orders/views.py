from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import datetime
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Order, OrderDetail, Cart, CartDetail, Coupon
from products.models import Product
from settings.models import DeliveryFee



# Create your views here.

def order_list(request):
    data = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders':data})


def checkout(request):
    cart = Cart.objects.get(user=request.user, status='Inprogress')
    cart_detail = CartDetail.objects.filter(cart=cart)
    delivery_fee = DeliveryFee.objects.last().fee


    # Add Coupon Befor ajax :
    # if request.method == 'POST' :
    #     code = request.POST['coupon_code']
    #     # coupon = Coupon.objects.get(code=code)
    #     coupon = get_object_or_404(Coupon,code=code)

    #     if coupon and coupon.quantity > 0 :
    #         today_date = datetime.datetime.today().date()
    #         if today_date >= coupon.start_date and today_date <= coupon.end_date :
    #             coupon_value = round(cart.cart_total / 100 * coupon.discount,2)
    #             sub_total = cart.cart_total - coupon_value
    #             total = sub_total + delivery_fee

    #             cart.coupon = coupon
    #             cart.total_with_coupon = sub_total
    #             cart.save()

    #             coupon.quantity -= 1
    #             coupon.save()

    #             return render (request, 'orders/checkout.html',{
    #             'cart_detail' : cart_detail,
    #             'delivery_fee' : delivery_fee,
    #             'sub_total' : sub_total,
    #             'discount' : coupon_value,
    #             'total' : total,
    #         })

    # sub_total = cart.cart_total
    # discount = 0
    # total = sub_total + delivery_fee

    # return render (request, 'orders/checkout.html',{
    #     'cart_detail' : cart_detail,
    #     'delivery_fee' : delivery_fee,
    #     'sub_total' : sub_total,
    #     'discount' : discount,
    #     'total' : total,
    #     })


    # Add Coupon Using ajax :
    if request.method == 'POST' :
        code = request.POST['coupon_code']
        # coupon = Coupon.objects.get(code=code)
        coupon = get_object_or_404(Coupon,code=code)

        if coupon and coupon.quantity > 0 :
            today_date = datetime.datetime.today().date()
            if today_date >= coupon.start_date and today_date <= coupon.end_date :
                coupon_value = round(cart.cart_total / 100 * coupon.discount,2)
                sub_total = cart.cart_total - coupon_value
                total = sub_total + delivery_fee

                cart.coupon = coupon
                cart.total_with_coupon = sub_total
                cart.save()

                coupon.quantity -= 1
                coupon.save()

                # Get data after save :
                cart = Cart.objects.get(user=request.user, status='Inprogress')
                cart_detail = CartDetail.objects.filter(cart=cart)
                sub_total = cart.cart_total
                if cart.coupon :
                    coupon_value = round(cart.cart_total / 100 * cart.coupon.discount,2)
                else :
                    coupon_value = 0
                total = sub_total + delivery_fee

                page = render_to_string('includes/checkout_detail.html', {
                    'cart_detail':cart_detail,
                    'delivery_fee':delivery_fee,
                    'sub_total':sub_total,
                    'discount':coupon_value,
                    'total':total,
                    })
                return JsonResponse({'result':page})

    sub_total = cart.cart_total
    if cart.coupon :
        coupon_value = round(cart.cart_total / 100 * cart.coupon.discount,2)
    else :
        coupon_value = 0

    total = sub_total + delivery_fee

    return render (request, 'orders/checkout.html',{
        'cart_detail' : cart_detail,
        'delivery_fee' : delivery_fee,
        'sub_total' : sub_total,
        'discount' : coupon_value,
        'total' : total,
        })


# Add To cart Before use ajax :

# def add_to_cart(request) :
#     product = Product.objects.get(id= request.POST['product_id'])
#     quantity = int(request.POST['quantity'])

#     cart = Cart.objects.get(user=request.user, status='Inprogress')
#     cart_detail , created = CartDetail.objects.get_or_create(cart=cart,product=product)

#     # if not created :
#     #     cart_detail.quantity = cart_detail.quantity + quantity

#     cart_detail.quantity = quantity
#     cart_detail.total = round(product.price * cart_detail.quantity , 2 )
#     cart_detail.save()

#     return redirect(f'/products/{product.slug}')




def add_to_cart(request) :
    product = Product.objects.get(id= request.POST['product_id'])
    quantity = int(request.POST['quantity'])

    cart = Cart.objects.get(user=request.user, status='Inprogress')
    cart_detail , created = CartDetail.objects.get_or_create(cart=cart,product=product)

    # if not created :
    #     cart_detail.quantity = cart_detail.quantity + quantity

    cart_detail.quantity = quantity
    cart_detail.total = round(product.price * cart_detail.quantity , 2 )
    cart_detail.save()

    
    # Get new data after create :
    cart = Cart.objects.get(user=request.user, status='Inprogress')
    cart_detail = CartDetail.objects.filter(cart=cart)
    total = cart.cart_total
    cart_count = len(cart_detail)

    page = render_to_string('includes/cart_detail.html', {'cart_data':cart , 'cart_detail_data':cart_detail,})
    return JsonResponse({'result':page,'total':total,'cart_count':cart_count,})