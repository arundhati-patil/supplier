from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Product, Order
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings


def send_whatsapp_message(phone, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{phone}",
        body=message
    )

def checkout(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        email = request.POST.get("email")
        products = request.POST.get("products")
        total_price = request.POST.get("total_price")



        customer_email = request.POST.get('email')  # Assuming email is collected in form
        subject = "Order Confirmation - SupplierHub"
        message = f"""
        Dear {name},
        
        Thank you for your order! We have received it and will process it soon.
        
        Here is your order summary:
        
        {products}
        
        Total Price: ₹{total_price}
        
        We will notify you once your order is shipped.

        Best regards,  
        SupplierHub Team
        """

        sender_email = "arundhatipatil58@gmail.com"  # Must match EMAIL_HOST_USER
        recipient_list = [customer_email]



        try:
            send_mail(subject, message, sender_email, recipient_list, fail_silently=False)
            return JsonResponse({"message": "Order placed & email sent successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return render(request, 'checkout.html')  # Render your checkout page


def home(request):
    products = [
        {"name": "Mask", "description": "Protective face mask", "price": 10, "image": "images/mask.jpeg", "availability": "In stock"},
        {"name": "Gloves", "description": "Trendy washable gloves", "price": 60, "image": "images/gloves.jpeg", "availability": "In stock"},
        {"name": "Cap", "description": "Comfortable cotton cap", "price": 100, "image": "images/cap.jpeg", "availability": "out of stock"},
        {"name": "Scarf", "description": "Stylish winter scarf", "price": 200, "image": "images/scraf.jpeg", "availability": "In stock"}
    ]
    return render(request, 'home.html', {'products': products})


