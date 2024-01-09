import flet as ft
import pyperclip as clip


def main(page: ft.Page) -> None:

    def copy_note(e: ft.ControlEvent) -> None:
        clip.copy(e.control.content.value)
        page.snack_bar.open = True
        page.update()

    def add_note(e: ft.ControlEvent) -> None:
        notes_row.controls.append(
            ft.Card(
                content = ft.Container(
                    content = ft.Text(note_text_field.value),
                    padding = 10,
                    on_click = copy_note
                ),
                col = {'md': 4, 'lg': 3},
            )
        )
        notes_row.update()
        note_text_field.value = ''
        note_text_field.update()


    note_text_field = ft.TextField(
        label = 'Enter a new note here...',
        max_length = 255,
        multiline = True,
        col = 8,
        suffix = ft.IconButton(icon = ft.icons.ARROW_DOWNWARD, on_click = add_note)
    )

    notes_row = ft.ResponsiveRow(
        
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.snack_bar = ft.SnackBar(
        content = ft.Text('Note copied to clipboard'),
        duration = 1000,
    )
    page.add(
        ft.Divider(opacity = 0),
        ft.ResponsiveRow(
            [
                note_text_field
            ],
            alignment = ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(opacity = 0),
        notes_row
    )
    page.update()


if __name__ == '__main__':
    ft.app(main)