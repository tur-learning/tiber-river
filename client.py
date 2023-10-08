import requests
import os
import json
import time
import zipfile

class OpenStreetMapClient:
    BASE_URL = "http://printmaps-osm.de:8282/api/beta2/maps"
    
    def __init__(self):
        pass
    
    def create_map_metadata(self, attributes: dict):
        url = f"{self.BASE_URL}/metadata"
        
        post_data = {
            "Data": {
                "Type": "maps",
                "ID": "",
                "Attributes": attributes
            }
        }
        
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/vnd.api+json; charset=utf-8",
                "Accept": "application/vnd.api+json; charset=utf-8",
            },
            data=json.dumps(post_data),
        )
        
        if response.status_code == 400:
            print("Error: Bad Request while creating map metadata. Stopping execution.")
            response.raise_for_status()  # This will raise an HTTPError and stop execution
        elif response.status_code == 201:
            print(f"Metadata succesfully created.")
        
        response.raise_for_status()  # Continue to raise for other unsuccessful status codes
        return response.json()
    
    def order_map(self, map_id: str):
        url = f"{self.BASE_URL}/mapfile"
        
        post_data = {
            "Data": {
                "Type": "maps",
                "ID": map_id
            }
        }
        
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/vnd.api+json; charset=utf-8",
                "Accept": "application/vnd.api+json; charset=utf-8",
            },
            data=json.dumps(post_data),
        )
        
        if response.status_code == 400:
            print("Error: Bad Request while creating an order. Stopping execution.")
            response.raise_for_status()  # This will raise an HTTPError and stop execution
        elif response.status_code == 202:
            print(f"Order succesfully accepted.")
        
        response.raise_for_status()  # Continue to raise for other unsuccessful status codes        
        return response.json()

    def fetch_map_state(self, map_id: str):
        url = f"{self.BASE_URL}/mapstate/{map_id}"
        
        response = requests.get(
            url,
            headers={"Accept": "application/vnd.api+json; charset=utf-8"},
            allow_redirects=False,
        )
        
        if response.status_code == 400:
            print("Error: Bad Request while fetching the status. Stopping execution.")
            response.raise_for_status()  # This will raise an HTTPError and stop execution
        elif response.status_code == 200:
            print(f"State succesfully fetched.")
        
        response.raise_for_status()  # Continue to raise for other unsuccessful status codes        
        return response.json()

    def download_map(self, map_id: str, output_dir: str = "."):
        url = f"{self.BASE_URL}/mapfile/{map_id}"
        
        response = requests.get(
            url,
            headers={"Accept": "application/vnd.api+json; charset=utf-8"},
        )
        
        if response.status_code == 400:
            print("Error: Bad Request while downloading the map. Stopping execution.")
            response.raise_for_status()  # This will raise an HTTPError and stop execution
        elif response.status_code == 200:
            print(f"Map succesfully downloaded.")
        
        response.raise_for_status()  # Continue to raise for other unsuccessful status codes       
            
        headers_filepath = os.path.join(output_dir, "response-header.txt")
        with open(headers_filepath, "w") as f:
            for key, value in response.headers.items():
                f.write(f"{key}: {value}\n")
        
        output_filepath = os.path.join(output_dir, "printmap.zip")
        with open(output_filepath, "wb") as f:
            f.write(response.content)
        
        print(f"Map downloaded successfully! Headers saved to {headers_filepath} and map to {output_filepath}")

        # Extracting the zip file
        zip_filepath = output_filepath
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        print(f"Map extracted to {output_dir}")
        
        # Removing the zip file
        os.remove(zip_filepath)
        print(f"{zip_filepath} removed.")

if __name__ == "__main__":
    client = OpenStreetMapClient()
    
    # Create map metadata
    attributes = {
        "Fileformat": "png",
        "Scale": 5000,
        "PrintWidth": 400,
        "PrintHeight": 1200,
        "Latitude": 41.89, #41.9149, #41.89
        "Longitude": 12.47, #12.4716, #12.47
        "Style": "osm-carto",
        "Projection": "3857",
        "HideLayers": "admin-low-zoom,admin-mid-zoom,admin-high-zoom,admin-text",
        "UserObjects": [
            #{ # Contorno Bianco
            #    "Style": "<PolygonSymbolizer fill='white' fill-opacity='1.0' />",
            #    "WellKnownText": "POLYGON((0.0 0.0, 0.0 600.0, 600.0 600.0, 600.0 0.0, 0.0 0.0), (20.0 20.0, 20.0 580.0, 580.0 580.0, 580.0 20.0, 20.0 20.0))"
            #},
            {
                "Style": "<LineSymbolizer stroke='dimgray' stroke-width='1.0' stroke-linecap='square' />",
                "WellKnownText": "LINESTRING(20.0 20.0, 20.0 580.0, 580.0 580.0, 580.0 20.0, 20.0 20.0)"
            },
            {
                "Style": "<LineSymbolizer stroke='dimgray' stroke-width='1.5' stroke-linecap='square' />",
                "WellKnownText": "MULTILINESTRING((5.0 0.0, 0.0 0.0, 0.0 5.0), (5.0 600.0, 0.0 600.0, 0.0 595.0), (595.0 600.0, 600.0 600.0, 600.0 595.0), (595.0 0.0, 600.0 0.0, 600.0 5.0))"
            },
            #{ # Scritta New York
            #    "Style": "<TextSymbolizer fontset-name='fontset-2' size='80' fill='dimgray' opacity='0.6' allow-overlap='true'>'New York'</TextSymbolizer>",
            #    "WellKnownText": "POINT(90.0 560.0)"
            #},
            {
                "Style": "<TextSymbolizer fontset-name='fontset-0' size='12' fill='dimgray' orientation='90' allow-overlap='true'>'© OpenStreetMap contributors'</TextSymbolizer>",
                "WellKnownText": "POINT(11 300.0)"
            }
        ]
    }
    
    metadata_response = client.create_map_metadata(attributes)
    print("...")
    print("Metadata Response:", metadata_response)
    
    # Assume the map_id is returned in the metadata response.
    map_id = metadata_response.get("Data", {}).get("ID", "")
    
    # Order the map.
    order_response = client.order_map(map_id)
    print("...")
    print(f"Order Response for {map_id}:", order_response)
    
    # Initialize variables
    map_build_successful = "no"
    timeout_minutes = 5
    timeout_sleep = int(timeout_minutes)
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60
    
    while map_build_successful != "yes" and (time.time() - start_time) < timeout_seconds:
        map_state = client.fetch_map_state(map_id)
        map_build_successful = map_state.get("Data", {}).get("Attributes", {}).get("MapBuildSuccessful", "no")
        
        if map_build_successful != "yes":
            print(f"Build ({map_id}) not successful yet, waiting for {timeout_sleep} second...")
            time.sleep(timeout_sleep)
    
    if map_build_successful == "yes":
        print("Build is successful, downloading the map...")
        print("...")
        print(f"Map State for {map_id}:", map_state)
        client.download_map(map_id)
    else:
        print(f"Build was not successful within {timeout_minutes} minutes.")