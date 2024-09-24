import ee
import json
import sys

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='ee-ventador')

def cloud_mask(image):
    # Mask both opaque and cirrus clouds
    mask = image.mask()

    # Get the band names for the image (server-side)
    band_names = image.bandNames()

    # Check and apply MSK_CLASSI_OPAQUE cloud masking if it exists
    mask = ee.Image(ee.Algorithms.If(
        band_names.contains('MSK_CLASSI_OPAQUE'),
        mask.And(image.select('MSK_CLASSI_OPAQUE').lt(1)),
        mask
    ))
    
    # Check and apply MSK_CLASSI_CIRRUS cloud masking if it exists
    mask = ee.Image(ee.Algorithms.If(
        band_names.contains('MSK_CLASSI_CIRRUS'),
        mask.And(image.select('MSK_CLASSI_CIRRUS').lt(1)),
        mask
    ))
    
    # Fallback to QA60 cloud masking if it exists
    mask = ee.Image(ee.Algorithms.If(
        band_names.contains('QA60'),
        mask.And(image.select('QA60').lt(1)),
        mask
    ))
    
    # Fallback to QA10 cloud masking if it exists
    mask = ee.Image(ee.Algorithms.If(
        band_names.contains('QA10'),
        mask.And(image.select('QA10').lt(1)),
        mask
    ))

    # Apply the final combined mask to the image
    return image.updateMask(mask)

def get_nearest_image(geojson_polygon, date):
    try:
        # Load Sentinel-2 data
        collection = ee.ImageCollection('COPERNICUS/S2')\
            .filterBounds(ee.Geometry.Polygon(geojson_polygon))\
            .filterDate(ee.Date(date).advance(-30, 'days'), date)\
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))\
            .map(cloud_mask)\

        # Get the median image from the collection
        nearest_image = collection.median()

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

# Calculate EVI using built-in Earth Engine function
def calculate_evi(geojson_polygon, date1, date2):
    image1 = get_nearest_image(geojson_polygon, date1)
    image2 = get_nearest_image(geojson_polygon, date2)

    if not image1:
        print("No image found for date1")
        return None, None
    if not image2:
        print("No image found for date2")
        return None, None

    # Calculate EVI for both images using Earth Engine built-in function
    evi1 = image1.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
        {
            'NIR': image1.select('B8'),  # Near Infrared Band
            'RED': image1.select('B4'),  # Red Band
            'BLUE': image1.select('B2')  # Blue Band
        }
    ).rename('EVI')

    evi2 = image2.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
        {
            'NIR': image2.select('B8'),
            'RED': image2.select('B4'),
            'BLUE': image2.select('B2')
        }
    ).rename('EVI')

    # Mask EVI values within the provided polygon
    polygon_geom = ee.Geometry.Polygon(geojson_polygon)
    evi_masked1 = evi1.clip(polygon_geom)
    evi_masked2 = evi2.clip(polygon_geom)

    # Visualization parameters for EVI
    evi_params = {
        'min': -1,
        'max': 1,
        'palette': ['blue', 'white', 'green']
    }

    # Get map tile URLs for visualizing EVI results
    evi_map_id1 = ee.Image(evi_masked1).getMapId(evi_params)
    evi_map_id2 = ee.Image(evi_masked2).getMapId(evi_params)

    return evi_map_id1['tile_fetcher'].url_format, evi_map_id2['tile_fetcher'].url_format

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    try:
        geojson_polygon = json.loads(sys.argv[1])
        date1 = sys.argv[2]
        date2 = sys.argv[3]

        tile_url_date1, tile_url_date2 = calculate_evi(geojson_polygon, date1, date2)

        if tile_url_date1 and tile_url_date2:
            result = {
                "tile_url_date1": tile_url_date1,
                "tile_url_date2": tile_url_date2
            }
            print(json.dumps(result))
        else:
            print(json.dumps({"error": "EVI calculation failed"}))
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON decode error: {e}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)