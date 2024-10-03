from src.gui.widgets.shadow import CustomDropShadow

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QFont, QValidator
from PyQt5.QtCore import QObject, Qt

from typing import Union, Tuple


class CustomInputBox(QLineEdit):
    '''
    A custom input box that extends QLineEdit, providing additional styling and functionality.
    '''
    def __init__(self,
            parent: QObject,
            style_sheet: str,
            geometry: Tuple[int, int, int, int],
            placeholder: Union[str, None]=None,
            font: Union[QFont, None]=None,
            max_length: Union[int, None]=None,
            validator: Union[QValidator, None]=None,
            blur_radius: Union[int, None]=None,
            blur_offset: Union[Tuple[int, int], None]=None
        ) -> None:
        '''
        Initializes a CustomInputBox instance with the specified attributes.

        Args:
            parent (QObject): The parent widget for this input box.
            style_sheet (str): The stylesheet to apply for custom styling.
            geometry (Tuple[int, int, int, int]): The position and size of the input box (x, y, width, height).
            placeholder (Union[str, None]): Optional placeholder text displayed when the input box is empty.
            font (Union[QFont, None]): Optional font for customizing the text appearance.
            max_length (Union[int, None]): Optional maximum number of characters allowed in the input box.
            validator (Union[QValidator, None]): Optional validator to restrict input formats.
            blur_radius (Union[int, None]): Optional blur radius for the shadow effect.
            blur_offset (Union[Tuple[int, int], None]): Optional offset for the shadow effect (x, y).
        '''
        super().__init__(parent)

        self.setStyleSheet(style_sheet)
        self.setAlignment(Qt.AlignCenter)
        self.setClearButtonEnabled(True)
        self.setGeometry(*geometry)

        if placeholder:
            self.setPlaceholderText(placeholder)

        if font:
            self.setFont(font)

        if max_length:
            self.setMaxLength(max_length)    

        if validator:
            self.setValidator(validator)

        if blur_radius and blur_offset:
            self.setGraphicsEffect(CustomDropShadow(blur_radius, blur_offset))
