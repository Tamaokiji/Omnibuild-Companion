import json
import os

def load_character(name):
    # Standardizes the name to find the file 
    path = f"data/characters/{name.lower()}.json"
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def get_all_characters():
    """Returns a list of all character data objects in the data folder."""
    characters = []
    char_folder = "data/characters/"
    
    # Loop through every file in your data/characters folder 
    for filename in os.listdir(char_folder):
        if filename.endswith(".json"):
            char_name = filename.replace(".json", "")
            data = load_character(char_name)
            if data:
                characters.append(data)
    return characters