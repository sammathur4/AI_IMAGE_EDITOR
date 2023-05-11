import os
import zipfile
import numpy as np
from flask import Flask, request, make_response
from pymongo import MongoClient
from io import BytesIO
import base64
from rembg import remove
from PIL import Image

app = Flask(__name__)

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['image_db']
collection = db['images']


@app.route('/remove_background', methods=['POST'])
def remove_background():
    # Get the uploaded images
    files = request.files.getlist('image')
    original_images = []
    new_images = []

    # Create folders if they don't exist
    if not os.path.exists('user_images/original_images'):
        os.makedirs('user_images/original_images')
    if not os.path.exists('user_images/new_images'):
        os.makedirs('user_images/new_images')

    # Process each image using rembg
    for i, file in enumerate(files):
        img = Image.open(file)
        output = remove(np.array(img.convert('RGB')))

        # Save original image locally
        original_img_path = f'user_images/original_images/original_image_{i}.jpg'
        img.convert('RGB').save(original_img_path)

        # Save output image locally
        new_img_path = f'user_images/new_images/new_image_{i}.png'
        Image.fromarray(output).save(new_img_path)

        original_images.append(original_img_path)
        new_images.append(new_img_path)

    # If only one image was uploaded, return the processed image directly
    if len(new_images) == 1:
        output_img_path = new_images[0]
        with open(output_img_path, 'rb') as f:
            output_img_bytes = f.read()

        response = make_response(output_img_bytes)
        response.headers.set('Content-Type', 'image/png')
        return response

    # Otherwise, create a zip file containing all images
    zip_filename = '../past/processed_images.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for original_image_path, new_image_path in zip(original_images, new_images):
            zip_file.write(original_image_path, os.path.basename(original_image_path))
            zip_file.write(new_image_path, os.path.basename(new_image_path))

    # Create response with zip file
    with open(zip_filename, 'rb') as f:
        response_bytes = f.read()

    response = make_response(response_bytes)
    response.headers.set('Content-Type', 'application/zip')
    response.headers.set('Content-Disposition', 'attachment', filename=zip_filename)
    return response


if __name__ == '__main__':
    app.run()
