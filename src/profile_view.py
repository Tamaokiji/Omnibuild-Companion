import flet as ft

def get_profile_view(page: ft.Page):
    # This structure avoids problematic keyword arguments like 'alignment' inside Column
    profile_content = ft.Column(
        [
            ft.CircleAvatar(
                foreground_image_src="https://avatars.githubusercontent.com/u/50414599?v=4",
                content=ft.Text("LM"),
                radius=50,
            ),
            ft.Text("Logan Manyrath", size=25, weight="bold"),
            ft.Text("Software Developer | WWCC Student", color="grey"),
            ft.Divider(),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.SETTINGS),
                title=ft.Text("Application Settings"),
                subtitle=ft.Text("Manage your OmniBuild Companion preferences"),
            ),
        ]
    )
    
    return ft.Container(content=profile_content, padding=20)