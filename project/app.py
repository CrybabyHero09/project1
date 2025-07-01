from flask import Flask, render_template, request, jsonify
import rasterio
import numpy as np
import smtplib
import geopandas as gpd
from shapely.geometry import shape, mapping
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_aoi', methods=['POST'])
def submit_aoi():
    geojson = request.json['geojson']
    polygon = shape(geojson['geometry'])

    # Process NDVI Change
    def calculate_ndvi(path):
        with rasterio.open(path) as src:
            red = src.read(1).astype('float32')
            nir = src.read(3).astype('float32')
            ndvi = (nir - red) / (nir + red + 1e-6)
        return ndvi

    ndvi1 = calculate_ndvi('data/jan_image.tif')
    ndvi2 = calculate_ndvi('data/june_image.tif')
    diff = ndvi2 - ndvi1

    change_map = np.where(diff < -0.2, 1, 0)
    change_count = np.sum(change_map)

    # Alert if change exceeds threshold
    if change_count > 500:
        send_email_alert("Change detected in AOI")

    # Export dummy shapefile
    gdf = gpd.GeoDataFrame({'geometry': [polygon]}, crs="EPSG:4326")
    gdf.to_file("output/change_output.shp")

    return jsonify({"status": "success", "change_pixels": int(change_count)})


def send_email_alert(msg):
    server = smtplplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("your_email", "your_password")
    server.sendmail("your_email", "user@example.com", f"Subject: Alert\n\n{msg}")
    server.quit()

if __name__ == '__main__':
    app.run(debug=True)
