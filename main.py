import flet as ft
import json
import os
from src.utils import get_icon_path
from src.data_loader import get_all_characters

def main(page: ft.Page):
    # Basic App Setup
    page.title = "OmniBuild Companion v1.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # Setup Paths for Save Data
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROFILE_PATH = os.path.join(BASE_DIR, "data", "user_profile.json")

    # Load character data
    all_chars = get_all_characters()
    print(f"DEBUG: Data Loader found {len(all_chars)} characters.")

    # State tracking for filtering
    current_element_filter = "All"
    
    # Pre-initialize container controls so helper functions can reference them
    char_list = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=10)
    search_bar = ft.TextField(
        hint_text="Search characters...", 
        prefix_icon=ft.Icons.SEARCH,
        border_color="bluegrey700",
        focused_border_color="blue400"
    )
    
    # Helper to load profile data from the JSON file safely
    def load_profile_data():
        if os.path.exists(PROFILE_PATH):
            try:
                with open(PROFILE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading profile JSON: {e}")
        # Default fallback values matching your original display layout
        return {
            "username": "Logan Manyrath", 
            "region": "NA", 
            "favorite_character": "Aino"
        }

    # -------------------------------------------------------------
    # DETAIL DIALOG / MODAL MECHANICS
    # -------------------------------------------------------------
    def close_modal(e):
        detail_dialog.open = False
        page.update()

    detail_dialog = ft.AlertDialog(title=ft.Text("Character Info"), modal=False)
    page.overlay.append(detail_dialog)

    def open_character_details(char):
        """Builds and opens a clean detail popup modal for a character."""
        builds = char.get('recommended_builds', [])
        build = builds[0] if builds else {}
        
        team_list = build.get('teams', [])
        team_controls = [ft.Text(f"• {team}", size=14, color="white") for team in team_list]
        if not team_controls:
            team_controls.append(ft.Text("• None listed", size=14, color="grey400"))

        artifacts_raw = build.get('artifacts', 'None listed')
        artifacts_str = ", ".join(artifacts_raw) if isinstance(artifacts_raw, list) else artifacts_raw

        detail_dialog.title = None 
        detail_dialog.content = ft.Container(
            width=450,
            padding=10,
            content=ft.Column([
                ft.Row([
                    ft.Text(char.get('name', 'Unknown'), size=26, weight="bold", color="white"),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color="grey400", on_click=close_modal)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=10, color="bluegrey800"),
                ft.Text(f"Element: {char.get('element', 'None')}", size=15, color="blue200"),
                ft.Text(f"Weapon Type: {char.get('weapon', 'None')}", size=15, color="blue200"),
                ft.Text(f"Build Role: {build.get('name', 'General Layout')}", size=15, color="bluegrey100", weight="bold"),
                ft.Text("Recommended Artifacts:", size=13, color="bluegrey300", weight="bold"),
                ft.Text(artifacts_str, size=13, italic=True, color="white"),
                ft.Text("Stat Priorities:", size=13, color="bluegrey300", weight="bold"),
                ft.Text(build.get('stats', 'Sands: ATK% | Goblet: DMG% | Circlet: CRIT'), size=13, color="white"),
                ft.Text("Optimal Team Compositions:", size=13, color="bluegrey300", weight="bold"),
                ft.Column(controls=team_controls, spacing=4),
            ], spacing=10, tight=True)
        )
        detail_dialog.open = True
        page.update()

    # -------------------------------------------------------------
    # FILTERING LOGIC
    # -------------------------------------------------------------
    def apply_filters():
        """Filters the display view based on Search Bar text and Element Chips."""
        search_term = search_bar.value.lower() if search_bar.value else ""
        char_list.controls.clear()
        
        for char in all_chars:
            name = char.get('name', 'Unknown')
            element = char.get('element', 'None')
            
            matches_search = search_term in name.lower()
            matches_element = (current_element_filter == "All" or element.lower() == current_element_filter.lower())
            
            if matches_search and matches_element:
                char_list.controls.append(
                    ft.Container(
                        bgcolor="#1e1e26",
                        border_radius=8,
                        on_click=lambda e, c=char: open_character_details(c),
                        content=ft.ListTile(
                            leading=ft.Image(src=get_icon_path(name), width=40, error_content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED)),
                            title=ft.Text(name, weight="bold", size=16),
                            subtitle=ft.Text(f"{element} | {char.get('weapon', 'None')}"),
                        )
                    )
                )
        char_list.update()

    def on_search_change(e):
        apply_filters()

    def on_element_click(e):
        nonlocal current_element_filter
        current_element_filter = e.control.content.value
        
        for container_btn in element_row.controls:
            text_inside = container_btn.content
            if text_inside.value == current_element_filter:
                text_inside.color = "blue400"
                container_btn.border = ft.Border.all(1, "blue400")
            else:
                text_inside.color = "white"
                container_btn.border = None
        element_row.update()
        apply_filters()

    # Create the filter chips strip layout
    elements = ["All", "Pyro", "Hydro", "Dendro", "Electro", "Geo", "Anemo", "Cryo"]
    # FIXED: Replaced custom layout spacing parameters with explicit margin-spaced containers inside the Row loop
    element_row = ft.Row(
        scroll=ft.ScrollMode.AUTO, 
        controls=[
            ft.Container(
                content=ft.Text(el, color="blue400" if el == "All" else "white", weight="bold"),
                padding=ft.Padding.symmetric(horizontal=12, vertical=6), 
                margin=ft.padding.only(right=8),
                border_radius=8,
                border=ft.Border.all(1, "blue400") if el == "All" else None, 
                on_click=on_element_click
            ) for el in elements
        ]
    )

    search_bar.on_change = on_search_change

    # -------------------------------------------------------------
    # NAVIGATION VIEWPORTS
    # -------------------------------------------------------------
    def show_library():
        page.vertical_alignment = "start" 
        page.horizontal_alignment = "start"
        page.controls.clear()
        
        page.add(
            ft.AppBar(
                title=ft.Text("OmniBuild Library"),
                bgcolor="#2d2d3a",
                actions=[
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: show_profile())
                ]
            ),
            search_bar,
            ft.Text("Filter by Element:", size=13, color="bluegrey300"),
            element_row,
            ft.Divider(height=15, thickness=1, color="bluegrey900"),
            char_list
        )
        apply_filters() 

    def show_profile():
        page.controls.clear()
        page.vertical_alignment = "start"
        page.horizontal_alignment = "start"
        
        # Load profile data from the JSON file to keep it unified
        current_profile = load_profile_data()

        # Dynamic profile header controls
        display_name = ft.Text(current_profile.get("username", "Logan Manyrath"), size=26, weight="bold", color="white")
        display_sub = ft.Text(
            f"Server: {current_profile.get('region', 'NA')} | Fav: {current_profile.get('favorite_character', 'Aino')}", 
            size=14, 
            color="bluegrey300"
        )

        # Real-time event handlers to link inputs to the header immediately
        def on_name_change(e):
            display_name.value = username_input.value if username_input.value else "Unnamed User"
            page.update()

        def on_meta_change(e):
            display_sub.value = f"Server: {region_dropdown.value} | Fav: {fav_input.value if fav_input.value else 'None'}"
            page.update()

        username_input = ft.TextField(
            label="Edit Profile Name", 
            value=current_profile.get("username", "Logan Manyrath"), 
            width=350, border_color="bluegrey700", focused_border_color="blue400",
            on_change=on_name_change
        )
        
        region_dropdown = ft.Dropdown(
            label="Game Server Region", 
            value=current_profile.get("region", "NA"), 
            width=350, border_color="bluegrey700", focused_border_color="blue400",
            options=[ft.dropdown.Option("NA"), ft.dropdown.Option("EU"), ft.dropdown.Option("ASIA"), ft.dropdown.Option("TW/HK/MO")],
            on_select=on_meta_change
        )
        
        fav_input = ft.TextField(
            label="Featured Character Favorite", 
            value=current_profile.get("favorite_character", "Aino"), 
            width=350, border_color="bluegrey700", focused_border_color="blue400",
            on_change=on_meta_change
        )

        def save_profile(e):
            updated_data = {
                "username": username_input.value,
                "region": region_dropdown.value,
                "favorite_character": fav_input.value
            }
            os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
            with open(PROFILE_PATH, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, indent=4)
                
            page.snack_bar = ft.SnackBar(ft.Text("Profile Changes Saved Permanently!"), open=True)
            page.update()

        # Reconstructed dynamic interface layout
        profile_content = ft.Container(
            padding=20,
            content=ft.Column([
                # Unified Header Block
                # FIXED: Stripped potential conflict arguments entirely from ft.Row and added a layout spacer container instead
                ft.Row([
                    ft.CircleAvatar(
                        radius=40,
                        bgcolor="bluegrey800",
                        content=ft.Icon(ft.Icons.PERSON, size=40, color="white")
                    ),
                    ft.Container(width=10), # Explicit visual space block
                    ft.Column([
                        display_name,
                        display_sub,
                        ft.Text("Software Developer | WWCC Student", size=12, color="bluegrey500")
                    ], spacing=4)
                ]),
                
                ft.Divider(height=30, color="bluegrey800"),
                
                # Settings header Section
                # FIXED: Removed all version-sensitive row-spacing keywords to protect cross-machine compilation
                ft.Row([
                    ft.Icon(ft.Icons.SETTINGS, color="bluegrey300", size=20),
                    ft.Container(width=5), # Explicit structural gap
                    ft.Column([
                        ft.Text("Application Settings", size=16, weight="bold", color="white"),
                        ft.Text("Manage your OmniBuild Companion preferences", size=13, color="bluegrey400")
                    ], spacing=2)
                ]),
                
                ft.Divider(height=10, color="transparent"),
                
                # Configuration Input Forms
                username_input, 
                region_dropdown, 
                fav_input,
                
                ft.Divider(height=10, color="transparent"),
                ft.ElevatedButton("Save Changes", on_click=save_profile, bgcolor="blue700", color="white", height=45)
            ], spacing=15)
        )

        page.add(
            ft.AppBar(
                title=ft.Text("User Profile"), 
                bgcolor="#2d2d3a",
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK, 
                    on_click=lambda _: show_library()
                )
            ),
            profile_content
        )
        page.update()

    # Start the app on the Library screen
    show_library()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
