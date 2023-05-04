import os
import random
import string
from django.shortcuts import render, redirect
from rembg import remove
from .forms import *
from .models import Image as ImageModel
from PIL import Image


def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['image']
            # Generate a random filename with a prefix and the original extension
            letters = string.ascii_letters
            prefix = "".join(random.sample(letters, 5))
            _, extension = os.path.splitext(uploaded_file.name)
            new_filename = f"{prefix}{extension}"

            # Build the file paths with the new filename
            file_path = f"images/{new_filename}"
            output_path = f"output/{prefix}.png"

            # Save the uploaded file with the new filename
            with open(file_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Process the image and save the output
            inputs = Image.open(file_path)
            output = remove(inputs)
            output.save(str(output_path))

            # Save the original image and the new image as model instances
            original_image = ImageModel(image=uploaded_file)
            original_image.save()

            new_image = ImageModel(image=output_path)
            new_image.save()

            # Get the URL of the new image and pass it to the template context
            new_image_url = new_image.image.url

            return render(request, 'image_upload.html', {'form': form, 'img_obj': new_image_url})

    else:
        return render(request, 'image_upload.html')


# import stripe
# from django.shortcuts import render, redirect
# from django.urls import reverse
# from django.conf import settings
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from googleapiclient.errors import HttpError
# from googleapiclient.discovery import build
#
# stripe.api_key = settings.STRIPE_SECRET_KEY
# GOOGLE_PAY_API_VERSION = 2
#
#
# def checkout(request):
#     if request.method == 'POST':
#         # Retrieve the token from the POST request
#         stripe_token = request.POST.get('stripeToken')
#
#         # Create a Stripe charge with the token
#         charge = stripe.Charge.create(
#             amount=1000,  # Amount in cents
#             currency='usd',
#             description='Example charge',
#             source=stripe_token
#         )
#
#         # Redirect to a success page if the charge was successful
#         if charge.paid:
#             return redirect(reverse('success'))
#
#     # Render the checkout page
#     return render(request, 'checkout.html', {
#         'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
#         'google_pay_merchant_id': settings.GOOGLE_PAY_MERCHANT_ID,
#     })
#
#
# def google_pay(request):
#     # Build the Google Pay API client
#     credentials = Credentials.from_authorized_user_info(info=request.user.auth_token)
#     service = build('payments', 'v1', credentials=credentials)
#
#     # Create a new payment request
#     payment_request = {
#         'apiVersion': GOOGLE_PAY_API_VERSION,
#         'apiVersionMinor': 0,
#         'allowedPaymentMethods': [{
#             'type': 'CARD',
#             'parameters': {
#                 'allowedAuthMethods': ['PAN_ONLY', 'CRYPTOGRAM_3DS'],
#                 'allowedCardNetworks': ['AMEX', 'DISCOVER', 'JCB', 'MASTERCARD', 'VISA'],
#             },
#             'tokenizationSpecification': {
#                 'type': 'PAYMENT_GATEWAY',
#                 'parameters': {
#                     'gateway': 'stripe',
#                     'stripe:version': '2020-08-27',
#                     'stripe:publishableKey': settings.STRIPE_PUBLISHABLE_KEY,
#                 },
#             },
#         }],
#         'transactionInfo': {
#             'totalPrice': '10.00',
#             'currencyCode': 'USD',
#             'countryCode': 'US',
#             'checkoutOption': 'COMPLETE_IMMEDIATE_PURCHASE',
#         },
#         'merchantInfo': {
#             'merchantName': 'Example Merchant',
#             'merchantId': settings.GOOGLE_PAY_MERCHANT_ID,
#         },
#     }
#
#     # Send the payment request to Google Pay
#     try:
#         payment_response = service.payments().create(body=payment_request).execute()
#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         payment_response = None
#
#     # Render the payment response
#     return render(request, 'google_pay.html', {
#         'payment_response': payment_response,
#     })

# def convert_image_format(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = request.FILES['image']
#             print("request.FILES['image']", request.FILES['image'])
#
#             # Generate a random filename with a prefix and the original extension
#             letters = string.ascii_letters
#             prefix = "".join(random.sample(letters, 5))
#             _, extension = os.path.splitext(uploaded_file.name)
#             new_filename = f"{prefix}{extension}"
#
#             # Build the file paths with the new filename
#             file_path = f"images/{new_filename}"
#             output_path = f"output/{prefix}.png"
#
#             # Save the uploaded file with the new filename
#             with open(file_path, 'wb+') as f:
#                 for chunk in uploaded_file.chunks():
#                     f.write(chunk)
#
#             # Process the image and save the output
#             inputs = Image.open(file_path)
#             #  Create document object
#             doc = aw.Document()
#             # Create a document builder object
#             builder = aw.DocumentBuilder(doc)
#
#             # Load and insert PNG image
#             shape = builder.insert_image(f"images/{new_filename}")
#
#             # Specify image save format as SVG
#             saveOptions = aw.saving.ImageSaveOptions(aw.SaveFormat.SVG)
#
#             # Save image as SVG
#             shape.get_shape_renderer().save(f"output/{prefix}.svg", saveOptions)
#
#             new_image = ImageModel(image=output_path)
#             new_image.save()
#
#             # Get the URL of the new image and pass it to the template context
#             new_image_url = new_image.image.url
#             return render(request, 'convert_image.html', {'form': form, 'img_obj': new_image_url})
#     else:
#         return render(request, 'convert_image.html')


# im = Image.open('NnoSb.png')
# im.save('test.tiff')


# This code example demonstrates how to convert PNG to SVG


# import stripe
# from django.conf import settings
# from django.shortcuts import redirect
# from django.views import View


# class CreateStripeCheckoutSessionView(View):
#     """
#     Create a checkout session and redirect the user to Stripe's checkout page
#     """
#
#     def post(self, request, *args, **kwargs):
#         price = Price.objects.get(id=self.kwargs["pk"])
#
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=["card"],
#             line_items=[
#                 {
#                     "price_data": {
#                         "currency": "usd",
#                         "unit_amount": int(price.price) * 100,
#                         "product_data": {
#                             "name": price.product.name,
#                             "description": price.product.desc,
#                             "images": [
#                                 f"{settings.BACKEND_DOMAIN}/{price.product.thumbnail}"
#                             ],
#                         },
#                     },
#                     "quantity": price.product.quantity,
#                 }
#             ],
#             metadata={"product_id": price.product.id},
#             mode="payment",
#             success_url=settings.PAYMENT_SUCCESS_URL,
#             cancel_url=settings.PAYMENT_CANCEL_URL,
#         )
#         return redirect(checkout_session.url)

#
#
#
# from django.views.generic import TemplateView
#
# class SuccessView(TemplateView):
#     template_name = "products/success.html"
#
# class CancelView(TemplateView):
#     template_name = "products/cancel.html"
