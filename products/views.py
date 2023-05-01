# from django.shortcuts import render
#
# # Create your views here.
#
#
# from django.shortcuts import render
# from .models import Payment
# import stripe
# from django.conf import settings
#
# stripe.api_key = settings.STRIPE_SECRET_KEY
# stripe_public_key = settings.STRIPE_PUBLIC_KEY
#
#
# def payment_view(request):
#     if request.method == 'POST':
#         amount = 50  # 50 pence
#         token = request.POST.get('stripeToken')
#         payment = Payment(amount=amount)
#         success = payment.process_payment(token)
#         if success:
#             # Payment successful - show success message
#             return render(request, 'payment_success.html')
#         else:
#             # Payment failed - show error message
#             return render(request, 'payment_error.html')
#     else:
#         return render(request, 'payment_form.html', {'stripe_public_key': stripe_public_key})
#
