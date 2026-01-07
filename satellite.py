import requests
import numpy as np
import cv2
import os
from fetch_image import fetch_gibs_image 
from landmarks import print_landmarks, add_new_landmark, landmarks
# BBOX Format: Min Lat, Min Long, Max Lat, Max Long


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