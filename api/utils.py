from PIL import Image
import numpy as np
from io import BytesIO
import requests

def convert_pixel_to_r5g6b5(pixel):
    r, g, b = pixel

    # Convert the color channels to 16-bit R5G6B5 format
    r5 = int(r * 31 / 255)  # Scale red channel to 5 bits
    g6 = int(g * 63 / 255)  # Scale green channel to 6 bits
    b5 = int(b * 31 / 255)  # Scale blue channel to 5 bits

    # Combine the channels into a single 16-bit value
    r5g6b5 = (r5 << 11) | (g6 << 5) | b5

    return r5g6b5


def convert_to_r5g6b5(image):
    """
    Convert image object to 16 bit R5G6B5 array value
    """
    # Load the image
    img = Image.open(BytesIO(image))
    
    # Convert the image to 16-bit R5G6B5 format
    img_rgb565 = img.convert("RGB")
    img_rgb565 = img_rgb565.resize((240, 240), Image.Resampling.LANCZOS)
    
    # Get the pixel data as a NumPy array
    img_array = np.array(img_rgb565)
    
    width, height = img_rgb565.size

    rgb565_array = []
    for y in range(height):
        for x in range(width):
            r, g, b = img_array[y,x]

            # convert the pixel to 16 bit rgb (red 5 bit, g 6 bit, b 5 bit) 
            # Convert the pixel to 16-bit RGB565
            rgb565_pixel = convert_pixel_to_r5g6b5((r, g, b))
            rgb565_array.append(rgb565_pixel)

    
    return rgb565_array