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

def calculate_ndii(geojson_polygon):
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

    # Select NIR and SWIR bands for NDII calculation
    NIR = sentinel2.select('B8')    # Near-infrared band
    SWIR = sentinel2.select('B11')  # Shortwave-infrared band
    
    # Apply NDII formula: (NIR - SWIR) / (NIR + SWIR)
    ndii = sentinel2.expression(
        '(NIR - SWIR) / (NIR + SWIR)',
        {
            'NIR': NIR,
            'SWIR': SWIR
        }
    ).rename('NDII')

    # Mask NDII to the polygon
    polygon_geom = ee.Geometry.Polygon(geojson_polygon)
    ndii_masked = ndii.clip(polygon_geom)

    # Define visualization parameters for NDII
    ndii_params = {
        'min': -1,
        'max': 1,
        'palette': ['brown', 'white', 'green']
    }

    # Get a URL for the NDII tile layer
    ndii_map_id = ee.Image(ndii_masked).getMapId(ndii_params)

    # Return the tile URL for NDII visualization
    return ndii_map_id['tile_fetcher'].url_format

if __name__ == "__main__":
    # Get coordinates from command-line arguments
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    try:
        geojson_polygon = json.loads(sys.argv[1])
        # Calculate NDII and print the result
        tile_url = calculate_ndii(geojson_polygon)
        print(json.dumps({"tile_url": tile_url}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
