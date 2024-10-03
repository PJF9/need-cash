from src.gui.widgets.shadow import CustomDropShadow
from src.gui.widgets.dial_window import CustomInfoWindow

from src.gui.utils.fonts import (
    see_flows_comment_font,
    trail_font,
    balance_header_font
)
from src.gui.utils.style_sheets import (
    trail_style_sheet,
    balance_label_style_sheet,
)

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import QObject, Qt, QEvent

from typing import Union, Tuple


class CustomLabel(QLabel):
    '''
    A QLabel with custom geometry, style, and optional drop shadow effect.
    '''
    def __init__(self,
            text: str,
            parent: QObject,
            geometry: Tuple[int, int, int, int],
            style_sheet: str,
            font: Union[QFont, None]=None,
            blur_radius: Union[int, None]=None,
            blur_offset: Union[Tuple[int, int], None]=None,
            hover_text: Union[str, None]=None,
            hover_style_sheet: Union[str, None]=None,
            hover_font: Union[str, None]=None
        ) -> None:
        '''
        Initializes the CustomLabel with the specified text, geometry, styles, and optional shadow effect.

        Args:
            text (str): The text to display on the label.
            parent (QObject): The parent object for the label.
            geometry (Tuple[int, int, int, int]): The geometry (x, y, width, height) of the label.
            style_sheet (str): The stylesheet to apply to the label.
            font (Union[QFont, None]): Optional font to apply to the label.
            blur_radius (Union[int, None]): Optional blur radius for the drop shadow effect.
            blur_offset (Union[Tuple[int, int], None]): Optional offset (x, y) for the drop shadow effect.
            hover_text (Union[str, None]): Text to display in a hover window when the mouse enters the label area (default is None).
            hover_style_sheet (Union[str, None]): Stylesheet to apply to the hover window (default is None).
            hover_font (Union[QFont, None]): Font to apply to the hover window text (default is None).
        '''
        super().__init__(text, parent)

        self.hover_text = hover_text
        self.hover_style_sheet = hover_style_sheet
        self.hover_font = hover_font

        # Set the stylesheet, geometry, and alignment for the label
        self.setStyleSheet(style_sheet)
        self.setGeometry(*geometry)
        self.setAlignment(Qt.AlignCenter)

        # Initialize the hover window reference
        self.hover_window = None

        if font:
            self.setFont(font)

        if blur_radius and blur_offset:
            self.setGraphicsEffect(CustomDropShadow(blur_radius, blur_offset))
    
    def enterEvent(self, event: QEvent) -> None:
        '''
        Event handler called when the mouse pointer enters the label area.
        Displays a hover window with the specified hover text, style, and font.

        Args:
            event (QEvent): The event object containing information about the hover event.
        '''
        if self.hover_text and self.hover_style_sheet:
            # Get the cursor position
            cursor_pos = QCursor.pos()
            
            # Create and show the info window at the cursor position
            self.hover_window = CustomInfoWindow(
                text=self.hover_text,
                style_sheet=self.hover_style_sheet,
                font=see_flows_comment_font
            )
            self.hover_window.move(cursor_pos.x() + 5, cursor_pos.y() + 5) # Offset the window slightly from the cursor
            self.hover_window.show()

        super().enterEvent(event)

    def leaveEvent(self, event):
        '''
        Event handler called when the mouse pointer leaves the label area.
        Closes the hover window if it is displayed.

        Args:
            event (QEvent): The event object containing information about the leave event.
        '''
        if self.hover_text and self.hover_style_sheet:
            self.hover_window.close()
            self.hover_window = None  # Clear the hover window reference

        super().leaveEvent(event)


class TrailLabel(CustomLabel):
    '''
    A label displaying flow and projection counts in a custom format with styles and shadow effects.
    '''
    def __init__(self,
            parent: QObject,
            account_name: str,
            n_flows: int,
            n_projections: int
        ) -> None:
        '''
        Initializes the TrailLabel with the number of flows and pending projections.

        Args:
            parent (QObject): The parent object for the label.
            account_name (str): The account name.
            n_flows (int): The number of flows to display.
            n_projections (int): The number of pending projections to display.
        '''
        super().__init__(
            text=f'{account_name} ({n_flows} flows - {n_projections} pending)',
            parent=parent,
            geometry=(0, 712, 1100, 40),
            style_sheet=trail_style_sheet,
            font=trail_font,
            blur_radius=5,
            blur_offset=(0, -2)
        )


class HeaderLabel(QWidget):
    '''
    HeaderLabel is a custom widget that creates and displays a balance label and a state label
    in a parent widget. It provides a visual representation of a monetary balance, along with an
    indicator on where the balance is going.
    '''
    def __init__(self,
            parent: QObject,
            state_style_sheet: str,
            balance: float
        ) -> None:
        '''
        Initializes the HeaderLabel widget.

        The initialization sets up two main labels:
        - A `CustomLabel` for displaying the balance with a given style, position, and font.
        - A `CustomLabel` for displaying the state label, styled by `state_style_sheet`.

        Args:
            parent (QObject): The parent widget where the HeaderLabel will be placed.
            state_style_sheet (str): The stylesheet used to define the appearance of the balance state label.
            balance (float): The monetary balance to display in the balance label.
        '''
        # Setting up the balance label
        CustomLabel(
            text=f'Balance: ${balance:.2f}',
            parent=parent,
            style_sheet=balance_label_style_sheet,
            geometry=(760, 10, 250, 80),
            font=balance_header_font,
            blur_radius=5,
            blur_offset=(5, 5)
        )

        # Setting up the balance state label
        balance_state_label = CustomLabel(
            text='',
            parent=parent,
            style_sheet=state_style_sheet,
            geometry=(760, 83, 250, 1),
        )
        balance_state_label.setFixedHeight(10)
