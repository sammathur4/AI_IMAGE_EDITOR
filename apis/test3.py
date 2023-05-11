from PIL import Image, ImageDraw, ImageFont

# Set up the canvas
width, height = 500, 500
canvas = Image.new('RGBA', (width, height), (255, 255, 255, 255))
draw = ImageDraw.Draw(canvas)

# Set the font
font_size = 80
font = ImageFont.truetype("arial.ttf", font_size)

# Set the text and center it
text = "Imagify"
text_bbox = draw.textbbox((0, 0), text, font=font)
x = (width - text_bbox[2]) / 2
y = (height - text_bbox[3]) / 2

# Draw the text
draw.text((x, y), text, fill=(0, 0, 0), font=font)

# Save the image
canvas.save("logo.png")
