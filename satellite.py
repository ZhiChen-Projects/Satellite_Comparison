import requests
import numpy as np
import cv2
import os
from fetch_image import fetch_gibs_image 
from landmarks import print_landmarks, add_new_landmark, landmarks
from image_analysis import create_change_highlights
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
        img_past = fetch_gibs_image(date_one, bbox, name)
        img_present = fetch_gibs_image(date_two, bbox, name)

        if img_past is not None and img_present is not None:
            img_comparison = create_change_highlights(img_past, img_present)
            
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img_past, "PAST", (20, 60), font, 1.1, (0,0,0), 2)
            cv2.putText(img_present, "RECENT", (20, 60), font, 1.1, (0,0,0), 2)
            cv2.putText(img_comparison, "CHANGE (RED)", (20, 60), font, 1.1, (0,0,255), 2)

            combined = np.hstack((img_past, img_present, img_comparison))
            

            cv2.line(combined, (800, 0), (800, 800), (0, 0, 0), 4)
            cv2.line(combined, (1600, 0), (1600, 800), (0, 0, 0), 4)

            # Save
            file_path = os.path.join(output_folder, f"{name}_analysis.jpg")
            cv2.imwrite(file_path, combined)
            print(f"Saved Analysis: {file_path}")

    print(f"\nFinished. Results are in the '{output_folder}' folder.")

if __name__ == "__main__":
    main()