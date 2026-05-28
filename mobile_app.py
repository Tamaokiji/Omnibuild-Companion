import flet as ft
import json
import os

def main(page: ft.Page):
    page.title = "Genshin Impact Build Guide"
    page.theme_mode = "dark"
    page.padding = 20
    page.scroll = "auto"

    # Paths
    BASE_DIR = os.path.dirname(__file__)
    data_path = os.path.join(BASE_DIR, "data", "characters")
    profile_file = os.path.join(BASE_DIR, "data", "user_profile.json")

    # Tracking states
    current_view = "Library"
    current_element_filter = "All"
    all_characters_data = []

    # Ensure data directory exists
    os.makedirs(os.path.dirname(profile_file), exist_ok=True)

    # 1. Load data
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

    def format_field(build, field_name):
        val = build.get(field_name, "None listed")
        if isinstance(val, list):
            return ", ".join(val)
        return val

    # 2. Detail Modal Logic
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
            width=400, padding=10,
            content=ft.Column([
                ft.Row([
                    ft.Text(data['name'], size=28, weight="bold", color="white"),
                    ft.Container(content=ft.Text("X", size=14, weight="bold", color="grey400"), on_click=close_modal, padding=5)
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

    # Character Card Builder
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
            bgcolor="#1e1e26", border_radius=12, padding=15,
            on_click=lambda e: open_character_details(data)
        )

    character_list_view = ft.ListView(expand=True, spacing=12, padding=10)

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

    search_bar = ft.TextField(hint_text="Search characters...", border_color="bluegrey700", focused_border_color="blue400", on_change=lambda e: apply_filters())
    elements = ["All", "Pyro", "Hydro", "Dendro", "Electro", "Geo", "Anemo", "Cryo"]
    
    def on_element_click(e):
        nonlocal current_element_filter
        current_element_filter = e.control.content.value
        for container_btn in element_row.controls:
            text_inside = container_btn.content
            text_inside.color = "blue400" if text_inside.value == current_element_filter else "white"
            container_btn.border = ft.border.all(1, "blue400") if text_inside.value == current_element_filter else None
        element_row.update()
        apply_filters()

    element_row = ft.Row(scroll="auto", spacing=8, controls=[
        ft.Container(content=ft.Text(el, color="blue400" if el == "All" else "white", weight="bold"),
                     padding=ft.padding.symmetric(horizontal=12, vertical=6), border_radius=8,
                     border=ft.border.all(1, "blue400") if el == "All" else None,
                     on_click=on_element_click) for el in elements
    ])

    # Dynamic Frame Containers
    view_wrapper = ft.Container(expand=True)

    def build_mobile_library():
        return ft.Column([
            ft.Text("Character Database", size=32, weight="bold"),
            search_bar,
            ft.Text("Filter by Element:", size=14, color="bluegrey300"),
            element_row,
            ft.Divider(height=20, thickness=1),
            character_list_view
        ], expand=True)

    def build_mobile_profile():
        profile = load_user_profile()
        
        username_input = ft.TextField(
            label="Profile Name", 
            value=profile.get("username"),
            border_color="bluegrey700",
            focused_border_color="blue400",
            bgcolor="#14141a",
            width=350
        )
        region_dropdown = ft.Dropdown(
            label="Region", 
            value=profile.get("region"),
            border_color="bluegrey700",
            focused_border_color="blue400",
            bgcolor="#14141a",
            width=350,
            options=[ft.dropdown.Option("NA"), ft.dropdown.Option("EU"), ft.dropdown.Option("ASIA")]
        )
        fav_input = ft.TextField(
            label="Favorite Character", 
            value=profile.get("favorite_character"),
            border_color="bluegrey700",
            focused_border_color="blue400",
            bgcolor="#14141a",
            width=350
        )

        def save_profile(e):
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump({"username": username_input.value, "region": region_dropdown.value, "favorite_character": fav_input.value}, f, indent=4)
            page.snack_bar = ft.SnackBar(ft.Text("Profile Saved!"), open=True)
            page.update()

        # FIX: Replaced invalid ft.VerticalDivider(height=...) references with transparent standard ft.Divider components
        return ft.Column([
            ft.Text("User Profile", size=32, weight="bold"),
            ft.Divider(height=10, color="bluegrey800"),
            ft.Container(
                content=ft.Column([
                    ft.Text("Profile Setup", size=18, weight="bold", color="blue200"),
                    ft.Text("Adjust your regional and default dashboard settings.", size=13, color="bluegrey300"),
                    ft.Divider(height=10, color="transparent"),
                    username_input, 
                    region_dropdown, 
                    fav_input,
                    ft.Divider(height=5, color="transparent"),
                    ft.ElevatedButton("Save Changes", on_click=save_profile, bgcolor="blue700", color="white", height=45)
                ], spacing=15),
                bgcolor="#1e1e26",
                border_radius=16,
                padding=20,
            )
        ], expand=True)

    # Handle Navigation Changes
    def on_nav_change(e):
        nonlocal current_view
        if e.control.selected_index == 0:
            current_view = "Library"
            view_wrapper.content = build_mobile_library()
        else:
            current_view = "Profile"
            view_wrapper.content = build_mobile_profile()
        
        view_wrapper.update()
        if current_view == "Library": 
            apply_filters()

    page.navigation_bar = ft.NavigationBar(
        bgcolor="#14141a",
        selected_index=0,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.LIST_ALT_ROUNDED, label="Library"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_ROUNDED, label="Profile")
        ]
    )

    # Boot Sequence
    for data in all_characters_data:
        character_list_view.controls.append(create_character_card(data))
        
    view_wrapper.content = build_mobile_library()
    page.add(view_wrapper)

ft.app(target=main)