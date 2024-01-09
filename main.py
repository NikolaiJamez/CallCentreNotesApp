import flet as ft


def main(page: ft.Page) -> None:

    note_text_field = ft.TextField(
        label = 'Enter a new note here...',
        max_length = 255,
        multiline = True,
        col = 8,
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(
        ft.Divider(opacity = 0),
        ft.ResponsiveRow(
            [
                note_text_field
            ],
            alignment = ft.MainAxisAlignment.CENTER
        )
    )
    page.update()


if __name__ == '__main__':
    ft.app(main)