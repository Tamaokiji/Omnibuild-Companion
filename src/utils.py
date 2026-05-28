import os

# --- 1. DATA FORMATTING ---
def format_list(data):
    """
    Prevents ['Item 1'] brackets in UI.
    Example: ["Sword", "Claymore"] -> "Sword, Claymore"
    """
    if isinstance(data, list):
        return ', '.join(data)
    return data if data else "N/A"

# --- 2. ASSET PATHING ---
def get_icon_path(name):
    """
    Fixes the 'Raiden Shogun' image bug.
    Converts name to lowercase but keeps spaces to match your .png files.
    """
    if not name:
        return "icons/unknown.png"
    clean_name = name.lower().strip()
    return f"icons/{clean_name}.png"

# --- 3. SAFE DATA EXTRACTION ---
def get_nested_val(data, keys, default="N/A"):
    """
    Safely navigates JSON without crashing if a key is missing.
    Usage: get_nested_val(char_dict, ["recommended_builds", 0, "artifacts"])
    """
    try:
        for key in keys:
            data = data[key]
        return format_list(data)
    except (KeyError, IndexError, TypeError):
        return default

# --- 4. GAMING MATH (Optional but helpful) ---
def get_rarity_color(rarity):
    """Returns hex colors based on character/item rarity."""
    colors = {
        5: "#ffb13f", # Gold/Orange
        4: "#a256e1", # Purple
        3: "#5180cc"  # Blue
    }
    return colors.get(rarity, "#ffffff")