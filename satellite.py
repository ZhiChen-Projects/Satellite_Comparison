import requests
import numpy as np
import cv2
import os

def fetch_gibs_image(date, bbox, label):
    url = "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi"
    params = {
        "SERVICE": "WMS",
        "VERSION": "1.3.0",
        "REQUEST": "GetMap",
        "LAYERS": "MODIS_Terra_CorrectedReflectance_TrueColor",
        "TIME": date,
        "CRS": "EPSG:4326",
        "BBOX": bbox,
        "WIDTH": "800",
        "HEIGHT": "800",
        "FORMAT": "image/jpeg",
        "STYLES": ""
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if "image/jpeg" not in response.headers.get("Content-Type", ""):
            print(f"Data gap for {label} on {date}")
            return None
        img_array = np.frombuffer(response.content, np.uint8)
        return cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except Exception as ex:
        print(f"Connection error for {label}: {ex}")
        return None

# BBOX Format: Min Lat, Min Long, Max Lat, Max Long
landmarks = {
    "Aral_Sea": "43,57,47,61",
    "Dubai_Palm_Islands": "24.9,54.8,25.2,55.2",
    "Amazon_Deforestation": "-11,-64,-8,-61",
    "Las_Vegas_Growth": "35.8,-115.5,36.4,-114.8",
    "Grand_Canyon": "35.8,-114.0,36.5,-112.0" 
}

def print_landmarks():
    print("\nYour current landmarks consist of: ")
    for name in landmarks:
        print(f"- {name}")

def add_new_landmark():
    while True:
        choice = input("\nDo you want to add a new landmark? (yes/no): ").strip().lower()
        if choice != "yes":
            break
        
        name = input("Enter landmark name (use underscores for spaces): ").strip()
        print("Enter BBOX coordinates (Lat/Long). Tip: Use wider ranges to zoom out.")
        min_lat = input("Min Latitude: ")
        min_lon = input("Min Longitude: ")
        max_lat = input("Max Latitude: ")
        max_lon = input("Max Longitude: ")
        
        bbox_string = f"{min_lat},{min_lon},{max_lat},{max_lon}"
        landmarks[name] = bbox_string
        print(f"Added {name} successfully!")

def main():
    print_landmarks()
    add_new_landmark() 
    print("-" * 30)
    
    date_one = input("Enter a date (YYYY-MM-DD): ")
    date_two = input("Enter another date (YYYY-MM-DD): ")
    output_folder = "comparison"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for name, bbox in landmarks.items():
        print(f"Processing {name}...")
        
        img_past = fetch_gibs_image(date_one, bbox, name)
        img_present = fetch_gibs_image(date_two, bbox, name)

        if img_past is not None and img_present is not None:
            font = cv2.FONT_HERSHEY_DUPLEX
            black_color = (0, 0, 0)
            
            # Label
            cv2.putText(img_past, f"{name.replace('_', ' ')} {date_one}", (20, 60), font, 1.1, black_color, 2)
            cv2.putText(img_present, f"{name.replace('_', ' ')} {date_two}", (20, 60), font, 1.1, black_color, 2)

            # Combined the two images
            combined = np.hstack((img_past, img_present))
            cv2.line(combined, (800, 0), (800, 800), (0, 0, 0), 4)

            file_path = os.path.join(output_folder, f"{name}_comparison.jpg")
            cv2.imwrite(file_path, combined)
            print(f"Saved: {file_path}")
        else:
            print(f"Skipping {name}: Data not available.")

    print(f"\nFinished. Results are in the '{output_folder}' folder.")

if __name__ == "__main__":
    main()