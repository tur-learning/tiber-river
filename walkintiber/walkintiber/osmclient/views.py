# osmclient/views.py
from django.http import JsonResponse, HttpResponse
import requests
import os
from datetime import datetime  # Import the datetime module
import zipfile
import tempfile
from django.conf import settings  # Import Django settings module
from xml.etree import ElementTree

def get_osm(request):
    # Extract bbox from request parameters
    bbox = request.GET.get('bbox')

    if not bbox:
        return JsonResponse({'error': 'Missing bbox parameter'}, status=400)

    # Validate and parse the bbox coordinates
    try:
        coords = [float(coord) for coord in bbox.split(',')]
        if len(coords) != 4:
            raise ValueError("bbox should contain exactly 4 coordinates")
    except ValueError as e:
        return JsonResponse({'error': f'Invalid bbox format: {e}'}, status=400)

    # Create a bbox string with three decimal places and no other characters
    formatted_bbox = ''.join(['{:.3f}'.format(coord).replace('.', '') for coord in coords])

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string "YYYYMMDDHHMM"
    timestamp = now.strftime("%Y%m%d%H%M")

    # Generate the file name based on the provided pattern
    file_name = f'map{timestamp}_bbox{formatted_bbox}.osm'

    # Use ASSETS_DIR from your settings
    file_path = os.path.join(settings.ASSETS_DIR, file_name)

    # Make the request to OpenStreetMap
    osm_url = f"https://api.openstreetmap.org/api/0.6/map?bbox={','.join(map(str, coords))}"
    try:
        response = requests.get(osm_url)
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({'error': 'Error querying OpenStreetMap API', 'detail': str(e)}, status=500)

    # # TODO find out what can be done with this .xml response
    # # As the response from OSM is XML, we will forward it as received (as plain text)
    # return HttpResponse(response.content, content_type='application/xml')

    # Save the content to a file
    with open(file_path, 'wb') as file:
        file.write(response.content)

    # # TODO fins out hwo to manage, effectively, .zip archives
    # # Optional: If you want to compress the file into a ZIP
    # zip_file_path = os.path.join(settings.ASSETS_DIR, 'map_data.zip')  # you might want to generate unique names for each zip file
    # with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
    #     zip_file.write(file_path, os.path.basename(file_path))

    # # Now, you might want to delete the original .osm file after zipping
    # os.remove(file_path)

    # Respond with the path to the saved file, or directly serve the zip file, or any response you see fit.
    # Here we just send a JSON with the file's path
    return JsonResponse({'success': True, 'file_path': file_path}, status=200)

def get_osm_relations_ways(request):
    # Extract bbox from request parameters
    bbox = request.GET.get('bbox')

    if not bbox:
        return JsonResponse({'error': 'Missing bbox parameter'}, status=400)

    # Validate and parse the bbox coordinates
    try:
        coords = [float(coord) for coord in bbox.split(',')]
        if len(coords) != 4:
            raise ValueError("bbox should contain exactly 4 coordinates")
    except ValueError as e:
        return JsonResponse({'error': f'Invalid bbox format: {e}'}, status=400)

    # Define the Overpass API URL
    OVERPASS_URL = "http://overpass-api.de/api/interpreter"

    # Define the Overpass QL query
    minlat, minlon, maxlat, maxlon = coords
    query = f"""
    [out:xml][timeout:900];
    (
      way["highway"]({minlat},{minlon},{maxlat},{maxlon});
      relation["highway"]({minlat},{minlon},{maxlat},{maxlon});
    );
    out body;
    >;
    out skel qt;
    """

    # Make the request to Overpass API
    try:
        response = requests.get(OVERPASS_URL, params={'data': query})
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({'error': 'Error querying Overpass API', 'detail': str(e)}, status=500)

    # Create a bbox string with three decimal places and no other characters
    formatted_bbox = ''.join(['{:.3f}'.format(coord).replace('.', '') for coord in coords])

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string "YYYYMMDDHHMM"
    timestamp = now.strftime("%Y%m%d%H%M")

    # Generate the file name based on the provided pattern
    file_name = f'map{timestamp}_bbox{formatted_bbox}.osm'
    file_path = os.path.join(settings.ASSETS_DIR, file_name)

    # Save the content to a file
    with open(file_path, 'wb') as file:
        file.write(response.content)

    # # Parse the OSM file and filter for highways
    # tree = ElementTree.parse(file_path)
    # root = tree.getroot()

    # Remove non-highway ways and relations from the tree
    # for element in root.findall('way'):
    #     highway_tag = False
    #     for tag in element.findall('tag'):
    #         if tag.get('k') == 'highway':
    #             highway_tag = True
    #             break
    #     if not highway_tag:
    #         print("element removed")
    #         root.remove(element)

    # for element in root.findall('relation'):
    #     highway_tag = False
    #     for tag in element.findall('tag'):
    #         if tag.get('k') == 'highway':
    #             highway_tag = True
    #             break
    #     if not highway_tag:
    #         root.remove(element)

    # # Write the filtered OSM data back to the file
    # tree.write(file_path+".new")

    # Respond with the path to the saved file
    return JsonResponse({'success': True, 'file_path': file_path}, status=200)

def get_osm_highways(request):
    # Extract bbox from request parameters
    bbox = request.GET.get('bbox')

    if not bbox:
        return JsonResponse({'error': 'Missing bbox parameter'}, status=400)

    # Validate and parse the bbox coordinates
    try:
        coords = [float(coord) for coord in bbox.split(',')]
        if len(coords) != 4:
            raise ValueError("bbox should contain exactly 4 coordinates")
    except ValueError as e:
        return JsonResponse({'error': f'Invalid bbox format: {e}'}, status=400)

   # Create a bbox string with three decimal places and no other characters
    formatted_bbox = ''.join(['{:.3f}'.format(coord).replace('.', '') for coord in coords])

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string "YYYYMMDDHHMM"
    timestamp = now.strftime("%Y%m%d%H%M")

    # Generate the file name based on the provided pattern
    file_name = f'map{timestamp}_bbox{formatted_bbox}.osm'
    file_path = os.path.join(settings.ASSETS_DIR, file_name)
    print("Ciao")

    # Make the request to the OSM API endpoint
    osm_url = f"https://api.openstreetmap.org/api/0.6/map?bbox={','.join(map(str, coords))}"
    try:
        response = requests.get(osm_url)
        response.raise_for_status()
        # Save the content to a file temporarily
        with open(file_path, 'wb') as file:
            file.write(response.content)
    except requests.RequestException as e:
        return JsonResponse({'error': 'Error querying OpenStreetMap API', 'detail': str(e)}, status=500)

    # Parse the OSM file and filter for highways
    tree = ElementTree.parse(file_path)
    root = tree.getroot()

    # Remove non-highway ways and relations from the tree
    for element in root.findall('way'):
        highway_tag = False
        for tag in element.findall('tag'):
            if tag.get('k') == 'highway' or tag.get('k') == 'bridge':
                highway_tag = True
                break
        if not highway_tag:
            root.remove(element)

    for element in root.findall('relation'):
        highway_tag = False
        for tag in element.findall('tag'):
            if tag.get('k') == 'highway' or tag.get('k') == 'bridge':
                highway_tag = True
                break
        if not highway_tag:
            root.remove(element)

    # Write the filtered OSM data back to the file
    tree.write(file_path+".new")

    # Respond with the path to the saved file
    return JsonResponse({'success': True, 'file_path': file_path}, status=200)


def post_osm_relations_ways(request):
    # Extract bbox from request parameters
    bbox = request.GET.get('bbox')

    if not bbox:
        return JsonResponse({'error': 'Missing bbox parameter'}, status=400)

    # Validate and parse the bbox coordinates
    try:
        coords = [float(coord) for coord in bbox.split(',')]
        if len(coords) != 4:
            raise ValueError("bbox should contain exactly 4 coordinates")
    except ValueError as e:
        return JsonResponse({'error': f'Invalid bbox format: {e}'}, status=400)

    # Define the Overpass API URL
    OVERPASS_URL = "http://overpass-api.de/api/interpreter"

    # Define the Overpass QL query
    minlat, minlon, maxlat, maxlon = coords
    query = f"""
    [out:xml][timeout:900];
    (
      way["highway"]({minlon},{minlat},{maxlon},{maxlat});
      relation["highway"]({minlon},{minlat},{maxlon},{maxlat});
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
        return JsonResponse({'error': 'Error querying Overpass API', 'detail': str(e)}, status=500)

    # Create a bbox string with three decimal places and no other characters
    formatted_bbox = ''.join(['{:.3f}'.format(coord).replace('.', '') for coord in coords])

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string "YYYYMMDDHHMM"
    timestamp = now.strftime("%Y%m%d%H%M")

    # Generate the file name based on the provided pattern
    file_name = f'map{timestamp}_bbox{formatted_bbox}.osm'
    file_path = os.path.join(settings.ASSETS_DIR, file_name)

    # Save the content to a file
    with open(file_path, 'wb') as file:
        file.write(response.content)

    # Respond with the path to the saved file
    return JsonResponse({'success': True, 'file_path': file_path}, status=200)
