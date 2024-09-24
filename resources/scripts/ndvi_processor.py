import ee
import json
import sys
import datetime

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='ee-ventador')

# Get the current date and calculate the start date (e.g., 1 month ago)
end_date = datetime.date.today().isoformat()
start_date = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()

def calculate_ndvi(geojson_polygon):
    # Load Sentinel-2 data with cloud masking
    def cloud_mask(image):
        # Mask both opaque and cirrus clouds
        opaque_clouds = image.select(['MSK_CLASSI_OPAQUE']).lt(1)
        cirrus_clouds = image.select(['MSK_CLASSI_CIRRUS']).lt(1)
        return image.updateMask(opaque_clouds).updateMask(cirrus_clouds)

    sentinel2 = ee.ImageCollection('COPERNICUS/S2')\
        .filterDate(start_date, end_date)\
        .filterBounds(ee.Geometry.Polygon(geojson_polygon))\
        .map(cloud_mask)\
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))\
        .median()

    # Calculate NDVI
    ndvi = sentinel2.normalizedDifference(['B8', 'B4']).rename('NDVI')

    # Mask NDVI to the polygon
    polygon_geom = ee.Geometry.Polygon(geojson_polygon)
    ndvi_masked = ndvi.clip(polygon_geom)

    # Define visualization parameters for NDVI
    ndvi_params = {
        'min': -0.2,
        'max': 0.8,  # Adjusted max value for better visualization
        'palette': ['blue', 'cyan', 'green', 'yellow', 'red'] # Enhanced color palette
    }

    # Get a URL for the NDVI tile layer
    ndvi_map_id = ee.Image(ndvi_masked).getMapId(ndvi_params)

    # Calculate the mean NDVI value over the polygon
    mean_ndvi = ndvi_masked.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=polygon_geom,
        scale=10  # Adjust scale as needed
    )

    # Get the average NDVI value
    avg_ndvi_value = mean_ndvi.get('NDVI').getInfo()

    # Return both the tile URL for NDVI visualization and the average NDVI value
    return ndvi_map_id['tile_fetcher'].url_format, avg_ndvi_value

if __name__ == "__main__":
    # Get coordinates from command-line arguments
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    try:
        geojson_polygon = json.loads(sys.argv[1])
        # Calculate NDVI and print the result
        tile_url, avg_ndvi_value = calculate_ndvi(geojson_polygon)
        print(json.dumps({"tile_url": tile_url, "avg_ndvi_value": avg_ndvi_value}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
