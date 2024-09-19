import ee
import json
import sys

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='ee-ventador')

def cloud_mask(image):
    # Initialize a mask as a full (true) mask
    mask = image.mask()  # Start with the full mask (all pixels valid)

    # Check for the presence of specific cloud masking bands
    if 'MSK_CLASSI_OPAQUE' in image.bandNames().getInfo():
        opaque_clouds = image.select(['MSK_CLASSI_OPAQUE']).lt(1)
        mask = mask.And(opaque_clouds)  # Update mask with opaque clouds
    
    if 'MSK_CLASSI_CIRRUS' in image.bandNames().getInfo():
        cirrus_clouds = image.select(['MSK_CLASSI_CIRRUS']).lt(1)
        mask = mask.And(cirrus_clouds)  # Update mask with cirrus clouds

    # Fallback to QA60 if necessary
    if 'QA60' in image.bandNames().getInfo():
        qa60_mask = image.select(['QA60']).lt(1)
        mask = mask.And(qa60_mask)  # Combine with QA60 mask

    # Optionally, you could also consider other QA bands like QA60
    if 'QA10' in image.bandNames().getInfo():  # Example: using QA10 for additional masking
        qa10_mask = image.select(['QA10']).lt(1)
        mask = mask.And(qa10_mask)  # Combine with QA10 mask

    # Apply the final combined mask to the image
    return image.updateMask(mask)



def get_nearest_image(geojson_polygon, date):
    try:
        # Load Sentinel-2 data
        collection = ee.ImageCollection('COPERNICUS/S2')\
            .filterBounds(ee.Geometry.Polygon(geojson_polygon))

        # Filter to find the nearest image before or on the specified date
        nearest_image = collection\
            .filterDate(ee.Date(date).advance(-5, 'days'), date)\
            .sort('system:time_start', False)\
            .first()

        # Check if we got an image
        image_info = nearest_image.getInfo()
        if image_info and 'bands' in image_info and len(image_info['bands']) > 0:
            return nearest_image
        else:
            print("No valid image or bands found.")
            return None
    except Exception as e:
        print(f"Error retrieving nearest image: {e}")
        return None

def compare_ndvi(geojson_polygon, date1, date2):
    image1 = get_nearest_image(geojson_polygon, date1)
    image2 = get_nearest_image(geojson_polygon, date2)

    if not image1:
        print("No image found for date1")
        return None, None
    if not image2:
        print("No image found for date2")
        return None, None

    # Apply cloud masking
    image1 = cloud_mask(image1)
    image2 = cloud_mask(image2)

    # Select NIR and Red bands for NDVI calculation
    NIR1 = image1.select('B8')
    red1 = image1.select('B4')
    NIR2 = image2.select('B8')
    red2 = image2.select('B4')

    # Apply NDVI formula
    ndvi1 = image1.expression(
        '(NIR - red) / (NIR + red)',
        {'NIR': NIR1, 'red': red1}
    ).rename('NDVI')

    ndvi2 = image2.expression(
        '(NIR - red) / (NIR + red)',
        {'NIR': NIR2, 'red': red2}
    ).rename('NDVI')

    # Mask NDVI to the polygon
    polygon_geom = ee.Geometry.Polygon(geojson_polygon)
    ndvi_masked1 = ndvi1.clip(polygon_geom)
    ndvi_masked2 = ndvi2.clip(polygon_geom)

    # Define visualization parameters
    ndvi_params = {
        'min': -1,
        'max': 1,
        'palette': ['brown', 'white', 'green']
    }

    # Get URLs for NDVI tile layers
    ndvi_map_id1 = ee.Image(ndvi_masked1).getMapId(ndvi_params)
    ndvi_map_id2 = ee.Image(ndvi_masked2).getMapId(ndvi_params)

    return ndvi_map_id1['tile_fetcher'].url_format, ndvi_map_id2['tile_fetcher'].url_format

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    try:
        geojson_polygon = json.loads(sys.argv[1])
        date1 = sys.argv[2]
        date2 = sys.argv[3]

        tile_url_date1, tile_url_date2 = compare_ndvi(geojson_polygon, date1, date2)

        if tile_url_date1 and tile_url_date2:
            result = {
                "tile_url_date1": tile_url_date1,
                "tile_url_date2": tile_url_date2
            }
            print(json.dumps(result))
        else:
            print(json.dumps({"error": "NDVI calculation failed"}))
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON decode error: {e}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
