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