from django.shortcuts import render,get_object_or_404,redirect
from .models import Payment , Product, Coupon
from .forms import ProductForm,CouponForm
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
import uuid
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import qrcode
import os
from django.conf import settings
from urllib.parse import unquote
from .forms import ContactForm
from django.contrib import messages


def index(request):
    return render(request,"layout.html")


def product_list(request):
    products = Product.objects.all()
    context = {
    'products': products
    }
    return render(request, 'product.html', context)

def course_list(request):
    products = Product.objects.all()
    context = {
    'products': products
    }
    return render(request, 'course.html', context)


def download_file(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    response = FileResponse(product.zipfile)
    return response


def initiate_payment_and_log(request, product_id, price,title):
    # Store values in session
    title = unquote(title)
    request.session['product_id'] = product_id
    request.session['price'] = price
    request.session['title'] = title
    print(title)
    # Call functions
    if request.method == "GET":  # Avoid infinite loop by using GET request for retry
        return initiate_payment(request)


@login_required
def initiate_payment(request):
    if request.method == "POST":
        price = request.session.get('price')
        product_id = request.session.get('product_id')
        title1 = request.session.get('title')
        copun_code = str(request.POST.get('copun_code'))
        if copun_code:
            try:
                # Validate coupon
                coupon = Coupon.objects.get(code=copun_code)
                if not coupon.is_active:
                    messages.error(request, "Coupon is not active.")
                    return redirect("initiate_payment")
                # Apply discount
                coupon_disct_price = int(coupon.discount)
                price = price - coupon_disct_price

            except Coupon.DoesNotExist:
                messages.error(request, "Coupon is not valid.")
                return redirect("initiate_payment")

        if not price or not product_id:
            return HttpResponse("Session expired or price not set!", status=400)

        # Generate unique order ID
        unique_id = str(uuid.uuid4().int)[:5]
        order_id = f"#order_id_{unique_id}"
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        copun_code = request.POST.get('copun_code')

        # Validate required fields
        if not all([customer_name, customer_email, customer_phone]):
            return HttpResponse("All customer details are required!", status=400)
        # Create Payment object and associate with the logged-in user
        payment = Payment(
            amount=price,
            order_id=order_id,
            title=title1,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            copun_code=copun_code,
            user=request.user  # Associate payment with user
        )
        payment.save()
        # Generate UPI link
        upi_link = f"upi://pay?pa=harishsuthar7023@oksbi&pn=TRADE_TOOL&am={price}&cu=INR"
        # Save QR code
        img_folder = os.path.join(settings.BASE_DIR, 'Trades', 'static', 'img')
        os.makedirs(img_folder, exist_ok=True)
        img_path = os.path.join(img_folder, 'googlepay_qr.png')
        qr = qrcode.make(upi_link)
        qr.save(img_path)
        return redirect("payment_success")

    return render(request, "payment_form.html")



@login_required
def user_payments(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    else:
        payments = None
    products = Product.objects.all()
    context = {
        'payments': payments,
        'products': products
    }
    return render(request, 'my_order.html', context)


def payment_success(request):
    return render(request,"qr.html")


def product_create_or_update(request, pk=None):
    if pk:
        product = get_object_or_404(Product, pk=pk)
    else:
        product = None
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')  # Redirect to your product listing page
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_add.html', {'form': form})


def manage_coupons(request):
    coupons = Coupon.objects.all()

    # Add Coupon Logic
    if request.method == 'POST' and 'add_coupon' in request.POST:
        add_form = CouponForm(request.POST)
        if add_form.is_valid():
            add_form.save()
            return redirect('manage_coupons')  # Reload the page after adding

    # Update Coupon Logic
    elif request.method == 'POST' and 'update_coupon' in request.POST:
        coupon_id = request.POST.get('coupon_id')
        coupon = Coupon.objects.get(id=coupon_id)
        update_form = CouponForm(request.POST, instance=coupon)
        if update_form.is_valid():
            update_form.save()
            return redirect('manage_coupons')  # Reload the page after updating

    else:
        add_form = CouponForm()

    return render(request, 'update_coupon.html', {
        'coupons': coupons,
        'add_form': add_form,
    })



def trade_home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Ye line data ko database me save karti hai
            return redirect('trade_home')
    else:
        form = ContactForm()
    products = Product.objects.all()

    context = {
        'form': form,
        'products': products
    }

    return render(request, 'home.html', context)



def about(request):
    return render(request, 'about.html')
