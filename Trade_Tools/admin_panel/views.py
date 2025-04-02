from django.shortcuts import render, get_object_or_404,redirect
from Trades.models import Payment,Product,Contact
from .models import VisitorCount
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.
from django.contrib.auth.decorators import login_required, user_passes_test

def product_list_admin(request):
    # payments = Payment.objects.filter(user=request.user)
    products = Product.objects.all()

    context = {
    # 'payments': payments,
    'products': products
    }
    # print(f"this is historys {historys}")  # Fetch all payment records
    return render(request, 'product_admin.html', context)



# Superuser check
def superuser_check(user):
    return user.is_superuser

# Apply superuser check to your view
@user_passes_test(superuser_check)
def dashboard_view(request):
    # Dashboard pe count show karna
    search_query = request.GET.get('search', '')

    if search_query:
        historys = Payment.objects.filter(
            Q(customer_name__icontains=search_query) | Q(title__icontains=search_query)
        )
    else:
        historys = Payment.objects.all().order_by('-created_at')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Render the filtered payment history and return as JSON
        html = render_to_string('payment_history_table.html', {'historys': historys})
        return JsonResponse({'html': html})

    Contacts = Contact.objects.all().order_by('-created_at')
    visitor_count, created = VisitorCount.objects.get_or_create(id=1)
    payment_status = "success"
    total_amount = Payment.objects.filter(payment_status=payment_status).aggregate(Sum('amount'))['amount__sum']
    total_users_count = User.objects.count()
    users_with_transactions_count = Payment.objects.filter(amount__gt=0, payment_status=payment_status).count()

    if total_amount is None:
        total_amount = 0.00

    context = {
        'Contacts': Contacts,
        'historys': historys,
        'visitor_count': visitor_count.count,
        'total_amount': total_amount,
        'total_users_count': total_users_count,
        'users_with_transactions_count': users_with_transactions_count
    }

    return render(request, 'dashboard.html', context)


def home_view(request):
    # Visitor count update karna
    visitor_count, created = VisitorCount.objects.get_or_create(id=1)
    visitor_count.count += 1
    visitor_count.save()

    # Sirf home.html render karna (dashboard yahan nahi)
    return render(request, 'home.html')


def dashboard(request):
    # Dashboard pe count show karna
    visitor_count, created = VisitorCount.objects.get_or_create(id=1)
    historys = Payment.objects.all()
    return render(request, 'dashboard.html', {'visitor_count': visitor_count.count})







@csrf_exempt  # Remove this if you are using {% csrf_token %}
def update_payment_status(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        payment_status = request.POST.get("payment_status")

        try:
            # Fetch the order and update its payment status
            order = Payment.objects.get(order_id=order_id)  # Replace `Order` with your actual model
            order.payment_status = payment_status
            order.save()

            # Redirect back to the same page after update
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirects to the previous page
        except Payment.DoesNotExist:
            return HttpResponse("Order not found.", status=404)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    return HttpResponse("Invalid request method.", status=405)

@csrf_exempt  # Remove this if you are using {% csrf_token %}
def update_payment_status2(request):
    if request.method == "POST":
        order_id = request.POST.get("pk")  # Get pk value
        # print(f"Received order_id: {order_id}")  # Debugging line
        try:
            contact = Contact.objects.get(pk=order_id)
            contact.delete()
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect back to the previous page
        except Contact.DoesNotExist:
            return HttpResponse("Order not found.", status=404)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

    return HttpResponse("Invalid request method.", status=405)


