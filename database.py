import json
import os 

DB_FIlE = "landmark_db.json"

LANDMARKS = {
    "Aral_Sea": "43,57,47,61",
    "Dubai_Palm_Islands": "24.9,54.8,25.2,55.2",
    "Amazon_Deforestation": "-11,-64,-8,-61",
    "Las_Vegas_Growth": "35.8,-115.5,36.4,-114.8",
    #"Grand_Canyon": "35.8,-114.0,36.5,-112.0" 
}

def load_landmarks():
    if not os.path.exists(DB_FIlE):
        print("Load landmarks from the JSON file.")
        save_landmarks(LANDMARKS)
        return LANDMARKS
    with open(DB_FIlE, 'r') as f:
        return json.load(f)


def save_landmarks(landmarks):
    with open(DB_FIlE, 'w') as f:
        json.dump(landmarks, f, indent=4)
    print("Landmarks saved to the JSON file.")