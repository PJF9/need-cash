from src.gui.widgets.label import CustomLabel
from src.gui.utils.fonts import progress_bar_font
from src.gui.utils.style_sheets import (
    progress_bar_placeholder_style_sheet,
    progress_bar_style_sheet,
    progress_bar_text_style_sheet
)

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject


class ProgressBarLabel(QWidget):
    '''
    A custom progress bar widget that displays a visual representation of a given percentage
    as a filled bar, along with a text label indicating the percentage.
    '''
    def __init__(self,
            parent: QObject,
            perc: int
        ) -> None:
        '''
        Initializes a ProgressBarLabel instance with the given parent and percentage value.

        Args:
            parent (QObject): The parent widget for this progress bar.
            perc (int): The percentage of progress to display, ranging from 0 to 100.

        This constructor sets up three components to represent the progress bar:
            1. A placeholder bar that acts as the background for the progress bar.
            2. A base bar that represents the actual progress and fills according to the given percentage.
            3. A label displaying the percentage value next to the bar.

        Styling and positioning of the components are handled using predefined stylesheets and fonts.
        '''
        # Setting the placeholder label
        placeholder = CustomLabel(
            text='',
            parent=parent,
            geometry=(280, 650, 500, 1),
            style_sheet=progress_bar_placeholder_style_sheet,
        )
        placeholder.setFixedHeight(20)

        # Setting the bar label
        base_bar = CustomLabel(
            text='',
            parent=parent,
            geometry=(280, 650, int(500 * perc/100), 1),
            style_sheet=progress_bar_style_sheet,
        )
        base_bar.setFixedHeight(20)

        # Setting the text label
        CustomLabel(
            text=f'{perc}%',
            parent=parent,
            geometry=(800, 645, 75, 30),
            style_sheet=progress_bar_text_style_sheet,
            font=progress_bar_font
        )
