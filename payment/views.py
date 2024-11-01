# from django.shortcuts import render

# Create your views here.

# payment/views.py
import razorpay
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


from django.core.mail import send_mail
from django.conf import settings

def send_booking_confirmation_email(user_email, booking_id):
    subject = 'Booking Confirmation'
    message = f'Your booking was successful! Your Booking ID is {booking_id}.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)


# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def payment_page(request):
    # Define the order amount and currency
    amount = 50000  # Amount in paise (INR 500)
    currency = 'INR'

    # Create Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='1'))

    # Send order details to the template
    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': amount,
    }

    return render(request, 'payment/payment_page.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        # Extract details from POST data
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')

        # Verify payment signature to ensure it's genuine
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)


            # Send booking confirmation email
            send_booking_confirmation_email('shalankhot1980@gmail.com', 'booking_888888888888')

            # If payment is verified, display success message
            return render(request, 'payment/success.html')
        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest("Payment verification failed")

    return HttpResponseBadRequest("Invalid request")

