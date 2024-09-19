import ee
import json
import sys

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='ee-ventador')

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

def calculate_evi(geojson_polygon, date1, date2):
    image1 = get_nearest_image(geojson_polygon, date1)
    image2 = get_nearest_image(geojson_polygon, date2)

    if not image1:
        print("No image found for date1")
        return None, None
    if not image2:
        print("No image found for date2")
        return None, None

    # EVI parameters
    G = 2.5
    C1 = 6
    C2 = 7.5
    L = 1

    # Select bands for EVI calculation
    NIR1 = image1.select('B8')
    RED1 = image1.select('B4')
    BLUE1 = image1.select('B2')
    
    NIR2 = image2.select('B8')
    RED2 = image2.select('B4')
    BLUE2 = image2.select('B2')

    # Apply EVI formula
    evi1 = image1.expression(
        'G * ((NIR - RED) / (NIR + C1 * RED - C2 * BLUE + L))',
        {'G': G, 'NIR': NIR1, 'RED': RED1, 'BLUE': BLUE1, 'C1': C1, 'C2': C2, 'L': L}
    ).rename('EVI')

    evi2 = image2.expression(
        'G * ((NIR - RED) / (NIR + C1 * RED - C2 * BLUE + L))',
        {'G': G, 'NIR': NIR2, 'RED': RED2, 'BLUE': BLUE2, 'C1': C1, 'C2': C2, 'L': L}
    ).rename('EVI')

    # Mask EVI to the polygon
    polygon_geom = ee.Geometry.Polygon(geojson_polygon)
    evi_masked1 = evi1.clip(polygon_geom)
    evi_masked2 = evi2.clip(polygon_geom)

    # Define visualization parameters
    evi_params = {
        'min': -1,
        'max': 1,
        'palette': ['blue', 'white', 'green']
    }

    # Get URLs for EVI tile layers
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
