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

def calculate_evi(geojson_polygon):
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

    # Calculate EVI using the formula:
    # EVI = G * (NIR - RED) / (NIR + C1 * RED - C2 * BLUE + L)
    G = 2.5
    C1 = 6
    C2 = 7.5
    L = 1
    NIR = sentinel2.select('B8')  # Near-infrared band
    RED = sentinel2.select('B4')  # Red band
    BLUE = sentinel2.select('B2') # Blue band
    
    # Apply EVI formula
    evi = sentinel2.expression(
        'G * ((NIR - RED) / (NIR + C1 * RED - C2 * BLUE + L))',
        {
            'G': G,
            'NIR': NIR,
            'RED': RED,
            'BLUE': BLUE,
            'C1': C1,
            'C2': C2,
            'L': L
        }
    ).rename('EVI')

    # Mask EVI to the polygon
    polygon_geom = ee.Geometry.Polygon(geojson_polygon)
    evi_masked = evi.clip(polygon_geom)

    # Define visualization parameters for EVI
    evi_params = {
        'min': -1,
        'max': 1,
        'palette': ['blue', 'white', 'green']
    }

    # Get a URL for the EVI tile layer
    evi_map_id = ee.Image(evi_masked).getMapId(evi_params)

    # Return the tile URL for EVI visualization
    return evi_map_id['tile_fetcher'].url_format

if __name__ == "__main__":
    # Get coordinates from command-line arguments
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    try:
        geojson_polygon = json.loads(sys.argv[1])
        # Calculate EVI and print the result
        tile_url = calculate_evi(geojson_polygon)
        print(json.dumps({"tile_url": tile_url}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
