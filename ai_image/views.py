import random

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# from .models import UploadImage
from .forms import ImageUploadForm
from .models import Image

import PIL.Image
import subprocess
from django.http import JsonResponse, HttpResponse
from rembg import remove
from PIL import Image
from .models import Image as ImageModel

# def remove_background(request):
#     if request.method == 'POST':
#         # Get the image from the request
#         image = request.FILES['image']
#
#         # Open the image with PIL
#         with Image.open(image) as pil_image:
#             # Convert the image to transparent PNG
#             im = pil_image.convert("RGBA")
#
#             # Create a white background
#             white = Image.new("RGB", pil_image.size, (255, 255, 255))
#             # white.paste(pil_image, mask=pil_image.split()[3])
#             # Save the image
#             white.save("transparent.png", "PNG")
#
#             # Use ImageMagick to remove the white background
#             subprocess.call(["magick", "convert", "transparent.png", "-transparent", "white", "no_bg.png"])
#             # Return the resulting image as a response
#             with open("no_bg.png", "rb") as image_file:
#                 return JsonResponse({'image': image_file.read().decode('latin-1')})
#
#     # Return an error if the request is not a POST request
#     else:
#         return render(request, 'image_upload.html')



#
# def image_upload(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = request.FILES['image']
#             # print(request.FILES['image']['InMemoryUploadedFile'])
#             print("request.FILES['image']", request.FILES['image'])
#
#             # Get the file path
#             import random
#             import string
#
#             # Randomly choose a letter from all the ascii_letters
#             letters = string.ascii_letters
#             uploaded_file_val = "".join(random.sample(letters, 5))
#
#             file_path = 'images/'+str(uploaded_file_val)
#             ans = random.randint(1, 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
#             output_path= 'output/'+str(ans)+'.png'
#             form.save()
#
#             # img_obj = form.instance
#             print("\n\n img_obj = form.instance, ",form.instance)
#             inputs = Image.open(file_path)
#             output = remove(inputs)
#             output.save(str(output_path))
#
#             # # Save the original image and the new image as model instances
#             # original_image = ImageModel(image=uploaded_file)
#             # original_image.save()
#             #
#             # new_image = ImageModel(image=output_path)
#             # new_image.save()
#
#             # # Return the output image as a response
#             # with open(output_path, 'rb') as f:
#             #     response = HttpResponse(f.read(), content_type='image/png')
#             #     response['Content-Disposition'] = 'inline; filename=output.png'
#             # return response
#
#             # Save the original image and the new image as model instances
#             original_image = ImageModel(image=uploaded_file)
#             original_image.save()
#
#             new_image = ImageModel(image=output_path)
#             new_image.save()
#
#             # Get the URL of the new image and pass it to the template context
#             new_image_url = new_image.image.url
#
#             return render(request, 'image_upload.html', {'form': form, 'img_obj': new_image_url})
#
#
#             # return render(request, 'image_upload.html', {'form': form, 'img_obj': output_path})
#     else:
#         # form = ImageForm()
#         return render(request, 'image_upload.html')


import os
import random
import string

from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image

from .forms import ImageUploadForm
from .models import Image as ImageModel
# from .remove_background import remove

def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['image']
            print("request.FILES['image']", request.FILES['image'])

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
