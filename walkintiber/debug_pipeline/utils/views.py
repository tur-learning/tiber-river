import requests
import os
from datetime import datetime  # Import the datetime module
import zipfile
import tempfile
import utils.settings as settings  # Import Django settings module
from xml.etree import ElementTree as ET

def get_highways(bbox):
    # Extract bbox from request parameters
    # bbox = request.GET.get('bbox')

    if not bbox:
        print('error: Missing bbox parameter')

    # Validate and parse the bbox coordinates
    try:
        coords = [float(coord) for coord in bbox.split(',')]
        if len(coords) != 4:
            raise ValueError("bbox should contain exactly 4 coordinates")
    except ValueError as e:
        print({'error': f'Invalid bbox format: {e}'})

    # Define the Overpass API URL
    OVERPASS_URL = "http://overpass-api.de/api/interpreter"

    # Define the Overpass QL query
    minlat, minlon, maxlat, maxlon = coords
    query = f"""
    [out:xml][timeout:900];
    (
      way["highway"]({minlat}, {minlon}, {maxlat}, {maxlon});
      relation["highway"]({minlat}, {minlon}, {maxlat}, {maxlon});
    );
    out body;
    >;
    out skel qt;
    """

    headers = {
        'Content-Type': 'application/osm3s+xml',
        'User-Agent': 'PostmanRuntime/7.34.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'overpass-api.de',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    # Make the request to Overpass API
    try:
        response = requests.post(OVERPASS_URL, data=query, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print({'error': 'Error querying Overpass API', 'detail': str(e)})
        
    # Create a bbox string with three decimal places and no other characters
    formatted_bbox = ''.join(['{:.3f}'.format(coord).replace('.', '') for coord in coords])

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string "YYYYMMDDHHMM"
    timestamp = now.strftime("%Y%m%d%H%M")

    # Generate the file name based on the provided pattern
    file_name = f'highway{timestamp}_bbox{formatted_bbox}.osm'
    file_path = os.path.join(settings.ASSETS_DIR, file_name)

    # Parse the XML response from Overpass API
    root = ET.fromstring(response.content)

    # Construct the bounds element
    bounds_attrib = {
        'minlat': str(minlat),
        'minlon': str(minlon),
        'maxlat': str(maxlat),
        'maxlon': str(maxlon)
    }
    bounds_element = ET.Element('bounds', bounds_attrib)

    # Insert the bounds element as the first child of the root (osm) element
    root.insert(1, bounds_element)

    # # Convert back to bytes
    # xml_content = ET.tostring(root, encoding='utf-8')

    # # Save the modified content to a file
    # with open(file_path, 'wb') as file:
    #     file.write(xml_content)

    # Save the content to a file
    with open(file_path, 'wb') as file:
        # file.write(response.content)
        # file.write(xml_content)
        ET.ElementTree(root).write(file, encoding='utf-8', xml_declaration=True)

    # Respond with the path to the saved file
    print({'success': True, 'file_path': file_path})

def get_buildings(bbox):
    # Extract bbox from request parameters
    # bbox = request.GET.get('bbox')

    if not bbox:
        print('error: Missing bbox parameter')

    # Validate and parse the bbox coordinates
    try:
        coords = [float(coord) for coord in bbox.split(',')]
        if len(coords) != 4:
            raise ValueError("bbox should contain exactly 4 coordinates")
    except ValueError as e:
        print({'error': f'Invalid bbox format: {e}'})

    # Define the Overpass API URL
    OVERPASS_URL = "http://overpass-api.de/api/interpreter"

    # Define the Overpass QL query for buildings
    minlat, minlon, maxlat, maxlon = coords
    query = f"""
    [out:xml][timeout:90];
    (
      way["building"]({minlat}, {minlon}, {maxlat}, {maxlon});
      relation["building"]({minlat}, {minlon}, {maxlat}, {maxlon});
    );
    out body;
    >;
    out skel qt;
    """

    headers = {
        'Content-Type': 'application/osm3s+xml'
    }

    # Make the request to Overpass API
    try:
        response = requests.post(OVERPASS_URL, data=query, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print({'error': 'Error querying Overpass API', 'detail': str(e)})
        
    # Create a bbox string with three decimal places and no other characters
    formatted_bbox = ''.join(['{:.3f}'.format(coord).replace('.', '') for coord in coords])

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string "YYYYMMDDHHMM"
    timestamp = now.strftime("%Y%m%d%H%M")

    # Generate the file name based on the provided pattern
    file_name = f'building{timestamp}_bbox{formatted_bbox}.osm'
    file_path = os.path.join(settings.ASSETS_DIR, file_name)

    # Parse the XML response from Overpass API
    root = ET.fromstring(response.content)

    # Construct the bounds element
    bounds_attrib = {
        'minlat': str(minlat),
        'minlon': str(minlon),
        'maxlat': str(maxlat),
        'maxlon': str(maxlon)
    }
    bounds_element = ET.Element('bounds', bounds_attrib)

    # Insert the bounds element as the first child of the root (osm) element
    root.insert(1, bounds_element)

    # # Convert back to bytes
    # xml_content = ET.tostring(root, encoding='utf-8')

    # # Save the modified content to a file
    # with open(file_path, 'wb') as file:
    #     file.write(xml_content)

    # Save the content to a file
    with open(file_path, 'wb') as file:
        # file.write(response.content)
        # file.write(xml_content)
        ET.ElementTree(root).write(file, encoding='utf-8', xml_declaration=True)

    # Respond with the path to the saved file
    print({'success': True, 'file_path': file_path})

def get_water(bbox):
    # Extract bbox from request parameters
    # bbox = request.GET.get('bbox')

    if not bbox:
        print('error: Missing bbox parameter')

    # Validate and parse the bbox coordinates
    try:
        coords = [float(coord) for coord in bbox.split(',')]
        if len(coords) != 4:
            raise ValueError("bbox should contain exactly 4 coordinates")
    except ValueError as e:
        print({'error': f'Invalid bbox format: {e}'})

    # Define the Overpass API URL
    OVERPASS_URL = "http://overpass-api.de/api/interpreter"

    # Define the Overpass QL query
    minlat, minlon, maxlat, maxlon = coords
    query = f"""
    [out:xml][timeout:900];
    (
      way["water"]({minlat}, {minlon}, {maxlat}, {maxlon});
      relation["water"]({minlat}, {minlon}, {maxlat}, {maxlon});
    );
    out body;
    >;
    out skel qt;
    """

    headers = {
        'Content-Type': 'application/osm3s+xml',
        'User-Agent': 'PostmanRuntime/7.34.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'overpass-api.de',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    # Make the request to Overpass API
    try:
        response = requests.post(OVERPASS_URL, data=query, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print({'error': 'Error querying Overpass API', 'detail': str(e)})
        
    # Create a bbox string with three decimal places and no other characters
    formatted_bbox = ''.join(['{:.3f}'.format(coord).replace('.', '') for coord in coords])

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string "YYYYMMDDHHMM"
    timestamp = now.strftime("%Y%m%d%H%M")

    # Generate the file name based on the provided pattern
    file_name = f'water{timestamp}_bbox{formatted_bbox}.osm'
    file_path = os.path.join(settings.ASSETS_DIR, file_name)

    # Parse the XML response from Overpass API
    root = ET.fromstring(response.content)

    # Construct the bounds element
    bounds_attrib = {
        'minlat': str(minlat),
        'minlon': str(minlon),
        'maxlat': str(maxlat),
        'maxlon': str(maxlon)
    }
    bounds_element = ET.Element('bounds', bounds_attrib)

    # Insert the bounds element as the first child of the root (osm) element
    root.insert(1, bounds_element)

    # # Convert back to bytes
    # xml_content = ET.tostring(root, encoding='utf-8')

    # # Save the modified content to a file
    # with open(file_path, 'wb') as file:
    #     file.write(xml_content)

    # Save the content to a file
    with open(file_path, 'wb') as file:
        # file.write(response.content)
        # file.write(xml_content)
        ET.ElementTree(root).write(file, encoding='utf-8', xml_declaration=True)

    # Respond with the path to the saved file
    print({'success': True, 'file_path': file_path})

def get_trees(bbox):
    # Extract bbox from request parameters
    # bbox = request.GET.get('bbox')

    if not bbox:
        print('error: Missing bbox parameter')

    # Validate and parse the bbox coordinates
    try:
        coords = [float(coord) for coord in bbox.split(',')]
        if len(coords) != 4:
            raise ValueError("bbox should contain exactly 4 coordinates")
    except ValueError as e:
        print({'error': f'Invalid bbox format: {e}'})

    # Define the Overpass API URL
    OVERPASS_URL = "http://overpass-api.de/api/interpreter"

    # Define the Overpass QL query
    minlat, minlon, maxlat, maxlon = coords
    query = f"""
    [out:xml][timeout:900];
    (
      node["natural"="tree"]({minlat}, {minlon}, {maxlat}, {maxlon});
      way["natural"="tree"]({minlat}, {minlon}, {maxlat}, {maxlon});
      relation["natural"="tree"]({minlat}, {minlon}, {maxlat}, {maxlon});
    );
    out body;
    >;
    out skel qt;
    """

    headers = {
        'Content-Type': 'application/osm3s+xml',
        'User-Agent': 'PostmanRuntime/7.34.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'overpass-api.de',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    # Make the request to Overpass API
    try:
        response = requests.post(OVERPASS_URL, data=query, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print({'error': 'Error querying Overpass API', 'detail': str(e)})
        
    # Create a bbox string with three decimal places and no other characters
    formatted_bbox = ''.join(['{:.3f}'.format(coord).replace('.', '') for coord in coords])

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string "YYYYMMDDHHMM"
    timestamp = now.strftime("%Y%m%d%H%M")

    # Generate the file name based on the provided pattern
    file_name = f'trees{timestamp}_bbox{formatted_bbox}.osm'
    file_path = os.path.join(settings.ASSETS_DIR, file_name)

    # Parse the XML response from Overpass API
    root = ET.fromstring(response.content)

    # Construct the bounds element
    bounds_attrib = {
        'minlat': str(minlat),
        'minlon': str(minlon),
        'maxlat': str(maxlat),
        'maxlon': str(maxlon)
    }
    bounds_element = ET.Element('bounds', bounds_attrib)

    # Insert the bounds element as the first child of the root (osm) element
    root.insert(1, bounds_element)

    # # Convert back to bytes
    # xml_content = ET.tostring(root, encoding='utf-8')

    # # Save the modified content to a file
    # with open(file_path, 'wb') as file:
    #     file.write(xml_content)

    # Save the content to a file
    with open(file_path, 'wb') as file:
        # file.write(response.content)
        # file.write(xml_content)
        ET.ElementTree(root).write(file, encoding='utf-8', xml_declaration=True)

    # Respond with the path to the saved file
    print({'success': True, 'file_path': file_path})

def get_osm(bbox = "41.88856,12.47106,41.89253,12.48202"):
    # bbox minlat, minlon, maxlat, maxlon
    print(bbox)
    get_buildings(bbox)
    get_highways(bbox)
    get_water(bbox)
    get_trees(bbox)