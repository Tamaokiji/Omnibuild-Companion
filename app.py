import flet as ft
import json
import os

def main(page: ft.Page):
    page.title = "Genshin Impact Companion Hub"
    page.theme_mode = "dark"
    page.padding = 30
    page.scroll = "auto"

    # Paths
    BASE_DIR = os.path.dirname(__file__)
    data_path = os.path.join(BASE_DIR, "data", "characters")
    profile_file = os.path.join(BASE_DIR, "data", "user_profile.json")

    # Track view state & active filters
    current_view = "Library"  # "Library" or "Profile"
    current_element_filter = "All"
    all_characters_data = []

    # Ensure data directory exists
    os.makedirs(os.path.dirname(profile_file), exist_ok=True)

    # 1. Load Data
    if os.path.exists(data_path):
        filenames = sorted(os.listdir(data_path))
        for filename in filenames:
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(data_path, filename), 'r', encoding='utf-8') as f:
                        all_characters_data.append(json.load(f))
                except Exception as e:
                    print(f"Error pre-loading {filename}: {e}")

    def load_user_profile():
        if os.path.exists(profile_file):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"username": "Traveler", "region": "NA", "favorite_character": "Aino"}

    # Helper to format lists or strings
    def format_field(build, field_name):
        val = build.get(field_name, "None listed")
        if isinstance(val, list):
            return ", ".join(val)
        return val

    # Detail Modal Logic
    def close_modal(e):
        detail_dialog.open = False
        page.update()

    detail_dialog = ft.AlertDialog(title=ft.Text("Character Info"), modal=False)
    page.overlay.append(detail_dialog)

    def open_character_details(data):
        builds = data.get('recommended_builds', [])
        build = builds[0] if builds else {}
        
        team_list = build.get('teams', [])
        team_controls = [ft.Text(f"• {team}", size=14, color="white") for team in team_list]
        if not team_controls:
            team_controls.append(ft.Text("• None listed", size=14, color="grey400"))

        detail_dialog.title = None 
        detail_dialog.content = ft.Container(
            width=500,
            padding=15,
            content=ft.Column([
                ft.Row([
                    ft.Text(data['name'], size=28, weight="bold", color="white"),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_color="grey400", on_click=close_modal)
                ], alignment="spaceBetween"),
                ft.Divider(height=10, color="bluegrey800"),
                ft.Text(f"Element: {data.get('element')}", size=16, color="blue200"),
                ft.Text(f"Weapon Type: {data.get('weapon')}", size=16, color="blue200"),
                ft.Text(f"Build Role: {build.get('name', 'General')}", size=16, color="bluegrey100", weight="bold"),
                ft.Text("Recommended Artifacts:", size=14, color="bluegrey300", weight="bold"),
                ft.Text(format_field(build, 'artifacts'), size=14, italic=True, color="white"),
                ft.Text("Stat Priorities:", size=14, color="bluegrey300", weight="bold"),
                ft.Text(build.get('stats', 'Sands: ATK% | Goblet: DMG% | Circlet: CRIT'), size=14, color="white"),
                ft.Text("Optimal Team Compositions:", size=14, color="bluegrey300", weight="bold"),
                ft.Column(controls=team_controls, spacing=4),
            ], spacing=12, tight=True)
        )
        detail_dialog.open = True
        detail_dialog.update()
        page.update()

    def create_character_card(data):
        character_image = f"icons/{data['name'].lower()}.png"
        builds = data.get('recommended_builds', [])
        build = builds[0] if builds else {}

        return ft.Container(
            content=ft.Row([
                ft.Image(src=character_image, width=75, height=120, fit="contain", error_content=ft.Container(bgcolor="grey900")),
                ft.VerticalDivider(width=10, color="transparent"),
                ft.Column([
                    ft.Text(data['name'], size=22, weight="bold", color="white"),
                    ft.Text(f"{data.get('element')} | {data.get('weapon')}", size=15, color="bluegrey100"),
                    ft.Text(f"Artifacts: {format_field(build, 'artifacts')}", size=13, italic=True, color="bluegrey200"),
                ], spacing=2, expand=True),
            ]),
            bgcolor="#1e1e26",
            border_radius=12,
            padding=15,
            on_click=lambda e: open_character_details(data)
        )

    character_list_view = ft.GridView(expand=True, runs_count=2, max_extent=400, child_aspect_ratio=2.5, spacing=15, run_spacing=15)

    def apply_filters():
        search_term = search_bar.value.lower() if search_bar.value else ""
        character_list_view.controls.clear()
        
        for data in all_characters_data:
            matches_search = search_term in data['name'].lower()
            char_element = data.get('element', '').lower()
            matches_element = (current_element_filter == "All" or char_element == current_element_filter.lower())
            
            if matches_search and matches_element:
                character_list_view.controls.append(create_character_card(data))
        character_list_view.update()

    def on_search_change(e): apply_filters()

    def on_element_click(e):
        nonlocal current_element_filter
        current_element_filter = e.control.content.value
        for container_btn in element_row.controls:
            text_inside = container_btn.content
            if text_inside.value == current_element_filter:
                text_inside.color, container_btn.border = "blue400", ft.border.all(1, "blue400")
            else:
                text_inside.color, container_btn.border = "white", None
        element_row.update()
        apply_filters()

    # Layout Elements
    search_bar = ft.TextField(hint_text="Search characters...", border_color="bluegrey700", focused_border_color="blue400", on_change=on_search_change)
    elements = ["All", "Pyro", "Hydro", "Dendro", "Electro", "Geo", "Anemo", "Cryo"]
    element_row = ft.Row(scroll="auto", spacing=8, controls=[
        ft.Container(content=ft.Text(el, color="blue400" if el == "All" else "white", weight="bold"),
                     padding=ft.Padding.symmetric(horizontal=12, vertical=6), border_radius=8,
                     border=ft.border.all(1, "blue400") if el == "All" else None, on_click=on_element_click) for el in elements
    ])

    # Core Container Layout Holder
    main_content_area = ft.Container(expand=True)

    def build_library_layout():
        return ft.Column([
            search_bar,
            ft.Text("Filter by Element:", size=14, color="bluegrey300"),
            element_row,
            ft.Divider(height=20, thickness=1, color="bluegrey900"),
            character_list_view
        ], expand=True)

    def build_profile_layout():
        profile = load_user_profile()
        username_input = ft.TextField(label="Profile Name", value=profile.get("username"), width=350)
        region_dropdown = ft.Dropdown(
            label="Game Server Region", value=profile.get("region"), width=350,
            options=[ft.dropdown.Option("NA"), ft.dropdown.Option("EU"), ft.dropdown.Option("ASIA"), ft.dropdown.Option("TW/HK/MO")]
        )
        fav_input = ft.TextField(label="Featured Character Favorite", value=profile.get("favorite_character"), width=350)

        def save_profile(e):
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump({"username": username_input.value, "region": region_dropdown.value, "favorite_character": fav_input.value}, f, indent=4)
            page.snack_bar = ft.SnackBar(ft.Text("Profile Saved Dynamically!"), open=True)
            page.update()

        # FIX: Removed the lowercase ft.alignment attribute block to avoid crashes
        return ft.Container(
            padding=30, bgcolor="#1e1e26", border_radius=16,
            content=ft.Column([
                ft.Text("User Profile Customization", size=24, weight="bold", color="white"),
                ft.Text("Manage dashboard defaults and tracker preferences.", size=14, color="bluegrey300"),
                ft.Divider(height=20, color="bluegrey800"),
                username_input, region_dropdown, fav_input,
                ft.ElevatedButton("Save Layout Profile", on_click=save_profile, bgcolor="blue700", color="white", height=45)
            ], spacing=20)
        )

    def change_view(view_name: str):
        nonlocal current_view
        current_view = view_name
        
        if current_view == "Library":
            library_btn.style = ft.ButtonStyle(color="blue400")
            profile_btn.style = ft.ButtonStyle(color="white")
            main_content_area.content = build_library_layout()
        else:
            library_btn.style = ft.ButtonStyle(color="white")
            profile_btn.style = ft.ButtonStyle(color="blue400")
            main_content_area.content = build_profile_layout()
            
        navigation_tabs.update()
        main_content_area.update()
        if current_view == "Library": 
            apply_filters()

    # Define buttons
    library_btn = ft.TextButton("Library", style=ft.ButtonStyle(color="blue400"), on_click=lambda e: change_view("Library"))
    profile_btn = ft.TextButton("User Profile", style=ft.ButtonStyle(color="white"), on_click=lambda e: change_view("Profile"))

    navigation_tabs = ft.Row([library_btn, profile_btn], spacing=10)

    # Boot Sequence
    for data in all_characters_data:
        character_list_view.controls.append(create_character_card(data))
    
    main_content_area.content = build_library_layout()

    page.add(
        ft.Row([
            ft.Text("Character Database", size=32, weight="bold", expand=True),
            navigation_tabs
        ], alignment="spaceBetween"),
        ft.Divider(height=10, color="transparent"),
        main_content_area
    )

ft.app(target=main)
