import flet as ft
from dataclasses import dataclass

@dataclass
class variables:
    SEPERATOR: str = '\n----------\n'
    FILENAME: str = 'notes.txt'


def main(page: ft.Page) -> None:

    def on_keyboard(e: ft.ControlEvent) -> None:
        if e.shift and e.key == 'Enter':
            add_note(e)

    def copy_note(e: ft.ControlEvent) -> None:
        page.set_clipboard(e.control.content.value)
        page.snack_bar.open = True
        page.update()

    def add_note(e: ft.ControlEvent) -> None:
        notes_row.controls.append(
            ft.Card(
                content = ft.Stack([
                    ft.Container(
                        content = ft.Text(note_text_field.value),
                        padding = 10,
                        on_click = copy_note,
                        data = len(notes_row.controls),
                    ),
                    ft.IconButton(
                        icon = ft.icons.CLOSE,
                        icon_color = ft.colors.RED,
                        right = 0,
                        scale = 0.5
                    ),
                ]),
                col = {'md': 4, 'lg': 3},
                tooltip = 'Click to copy',
            )
        )
        notes_row.update()
        note_text_field.value = ''
        note_text_field.update()

    def save_notes(e: ft.ControlEvent) -> None:
        with open(variables.FILENAME, 'w') as out_file:
            first = True
            for note in notes_row.controls:
                if not first:
                    out_file.writelines(variables.SEPERATOR)
                first = False
                out_file.writelines(note.content.controls[0].content.value)
    
    def load_notes(e: ft.ControlEvent = None) -> None:
        if len(notes_row.controls) > 0:
            notes_row.controls = []
        try:
            with open(variables.FILENAME, 'r') as in_file:
                note_texts = in_file.read().split(variables.SEPERATOR)
                for text in note_texts:
                    if not text:
                        continue
                    notes_row.controls.append(
                        ft.Card(
                            content = ft.Stack([
                                ft.Container(
                                    content = ft.Text(text),
                                    padding = 10,
                                    on_click = copy_note,
                                    data = len(notes_row.controls),
                                ),
                                ft.IconButton(
                                    icon = ft.icons.CLOSE,
                                    icon_color = ft.colors.RED,
                                    right = 0,
                                    scale = 0.5,
                                    on_click = delete_note
                                ),
                            ]),
                            col = {'md': 4, 'lg': 3},
                            tooltip = 'Click to copy',
                        )
                    )
                notes_row.update()
        except FileNotFoundError:
            return

    def delete_note(e: ft.ControlEvent) -> None:
        for id, control in enumerate(notes_row.controls):
            if control.content.data != e.control.data:
                continue
            notes_row.controls.pop(id)
            break
        notes_row.update()
    
    def delete_all_notes(e: ft.ControlEvent) -> None:
        notes_row.controls = []
        notes_row.update()

    def close_app(e: ft.ControlEvent) -> None:
        page.window_close()

            
    note_text_field = ft.TextField(
        label = 'Enter a new note here...',
        max_length = 255,
        multiline = True,
        col = 8,
        suffix = ft.IconButton(icon = ft.icons.ARROW_DOWNWARD, on_click = add_note)
    )

    notes_row = ft.ResponsiveRow()

    page.on_keyboard_event = on_keyboard
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.HIDDEN
    page.snack_bar = ft.SnackBar(
        content = ft.Text('Note copied to clipboard'),
        duration = 1000,
    )
    page.appbar = ft.AppBar(
        leading = ft.Icon(ft.icons.EDIT_NOTE),
        leading_width = 40,
        title = ft.Text("Call Center Notes Manager"),
        center_title = False,
        bgcolor = ft.colors.SURFACE_VARIANT,
        actions = [
            ft.IconButton(
                icon = ft.icons.SAVE,
                icon_color = ft.colors.GREEN,
                tooltip = 'Save Notes',
                on_click = save_notes
            ),
            ft.IconButton(
                icon = ft.icons.REFRESH,
                tooltip = 'Refresh Notes',
                on_click = load_notes
            ),
            ft.IconButton(
                icon = ft.icons.DELETE_FOREVER,
                icon_color = ft.colors.RED,
                tooltip = 'Delete All Notes',
                on_click = delete_all_notes
            ),
            ft.VerticalDivider(),
            ft.IconButton(
                icon = ft.icons.CLOSE,
                icon_color = ft.colors.RED,
                tooltip = 'Close App',
                on_click = close_app
            ),
        ],
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

    load_notes()
    page.update()


if __name__ == '__main__':
    ft.app(main)
