from database import load_landmarks, save_landmarks

landmarks = load_landmarks()


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
        save_landmarks(landmarks)
        print(f"Added {name} successfully!")