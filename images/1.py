
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
            # print("request.FILES['image']", request.FILES['image'])

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