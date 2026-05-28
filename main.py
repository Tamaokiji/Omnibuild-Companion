import flet as ft
from src.utils import get_icon_path
from src.data_loader import get_all_characters
from src.profile_view import get_profile_view

def main(page: ft.Page):
    # Basic App Setup
    page.title = "OmniBuild Companion v1.0"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Load character data
    all_chars = get_all_characters()
    print(f"DEBUG: Data Loader found {len(all_chars)} characters.")

    def show_library():
        # Standard alignment for the list view
        page.vertical_alignment = "start" 
        page.horizontal_alignment = "start"
        
        page.controls.clear()
        char_list = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
        
        for char in all_chars:
            name = char.get('name', 'Unknown')
            char_list.controls.append(
                ft.ListTile(
                    leading=ft.Image(src=get_icon_path(name), width=40),
                    title=ft.Text(name),
                    subtitle=ft.Text(f"{char.get('element', 'None')} | {char.get('weapon', 'None')}"),
                    bgcolor="#1e1e26",
                )
            )

        page.add(
            ft.AppBar(
                title=ft.Text("OmniBuild Library"),
                bgcolor="#2d2d3a",
                actions=[
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: show_profile())
                ]
            ),
            ft.TextField(hint_text="Search characters...", prefix_icon=ft.Icons.SEARCH),
            char_list
        )
        page.update()

    def show_profile():
        page.controls.clear()
        
        # Center the profile view using Page-level properties
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        
        page.add(
            ft.AppBar(
                title=ft.Text("User Profile"), 
                bgcolor="#2d2d3a",
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK, 
                    on_click=lambda _: show_library()
                )
            ),
            get_profile_view(page)
        )
        page.update()

    # Start the app on the Library screen
    show_library()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")