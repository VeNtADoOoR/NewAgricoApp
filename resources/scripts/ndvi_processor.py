import ee
import json
import sys

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='ee-ventador')

def calculate_ndvi(geojson_polygon):
    # Load Sentinel-2 data with cloud masking
    def cloud_mask(image):
        # Define cloud masking function
        cloud_mask = image.select(['QA60']).bitwiseAnd(1 << 10).eq(0)
        return image.updateMask(cloud_mask)

    sentinel2 = ee.ImageCollection('COPERNICUS/S2')\
        .filterDate('2023-01-01', '2023-01-31')\
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
        'palette': ['blue', 'cyan', 'green', 'yellow', 'red']  # Enhanced color palette
    }

    # Get a URL for the NDVI tile layer
    ndvi_map_id = ee.Image(ndvi_masked).getMapId(ndvi_params)

    # Return the tile URL for NDVI visualization
    return ndvi_map_id['tile_fetcher'].url_format

if __name__ == "__main__":
    # Get coordinates from command-line arguments
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    try:
        geojson_polygon = json.loads(sys.argv[1])
        # Calculate NDVI and print the result
        tile_url = calculate_ndvi(geojson_polygon)
        print(json.dumps({"tile_url": tile_url}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
