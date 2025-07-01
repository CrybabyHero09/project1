import numpy as np
import rasterio
from rasterio.transform import from_origin
import os

os.makedirs("data", exist_ok=True)

width = height = 100  # image size
transform = from_origin(77.0, 28.0, 0.01, 0.01)  # top-left x/y, pixel width/height

# Create Jan Image
jan_bands = [
    np.random.randint(50, 150, (height, width), dtype='uint8'),  # Red
    np.random.randint(50, 150, (height, width), dtype='uint8'),  # Green
    np.random.randint(50, 150, (height, width), dtype='uint8')   # NIR
]

with rasterio.open('data/jan_image.tif', 'w', driver='GTiff',
                   height=height, width=width, count=3, dtype='uint8',
                   crs='EPSG:4326', transform=transform) as dst:
    for i, band in enumerate(jan_bands):
        dst.write(band, i + 1)

# Create June Image with more vegetation (higher NIR)
june_bands = [
    jan_bands[0],  # Red same
    jan_bands[1],  # Green same
    jan_bands[2] + 20  # Boost NIR for change
]

with rasterio.open('data/june_image.tif', 'w', driver='GTiff',
                   height=height, width=width, count=3, dtype='uint8',
                   crs='EPSG:4326', transform=transform) as dst:
    for i, band in enumerate(june_bands):
        dst.write(band, i + 1)

print("✅ Dummy satellite images saved to /data.")
