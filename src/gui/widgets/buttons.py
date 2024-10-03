from src.gui.widgets.shadow import CustomDropShadow

from PyQt5.QtWidgets import QPushButton, QToolButton
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QObject, Qt

from typing import Union, Tuple, Callable


class CustomPushButton(QPushButton):
    '''
    A QPushButton with customizable size, position, style, and optional click event and drop shadow effect.
    '''
    def __init__(self,
            text: str,
            parent: QObject,
            size: Tuple[int, int],
            pos: Tuple[int, int],
            style_sheet: str,
            font: Union[QFont, None]=None,
            blur_radius: Union[int, None]=None,
            blur_offset: Union[Tuple[int, int], None]=None,
            on_click: Union[Callable[..., None], None]=None
        ) -> None:
        '''
        Initializes the CustomPushButton with the specified text, size, position, style, and optional click event.

        Args:
            text (str): The button label text.
            parent (QObject): The parent object for the button.
            size (Tuple[int, int]): The width and height of the button.
            pos (Tuple[int, int]): The X and Y position of the button.
            style_sheet (str): The stylesheet to apply to the button.
            font (Union[QFont, None]): Optional font to apply to the button.
            blur_radius (Union[int, None]): Optional blur radius for the drop shadow effect.
            blur_offset (Union[Tuple[int, int], None]): Optional offset (x, y) for the drop shadow effect.
            on_click (Union[Callable[..., None], None]): Optional callback function for the button's clicked signal.
        '''
        super().__init__(text, parent)
        self.setFixedSize(*size)
        self.move(*pos)
        self.setStyleSheet(style_sheet)

        if font:
            self.setFont(font)

        if blur_radius and blur_offset:
            self.setGraphicsEffect(CustomDropShadow(blur_radius, blur_offset, QColor(63, 63, 63, 180))) # Semi-transparent shadow

        if on_click:
            self.clicked.connect(on_click)


class CustomToolButton(QToolButton):
    '''
    A custom QToolButton with an arrow (left or right), customizable size, style, and optional click event and shadow effect.
    '''
    def __init__(self, 
            parent: QObject,
            size: Tuple[int, int],
            pos: Tuple[int, int],
            style_sheet: str,
            is_right: bool,
            font: Union[QFont, None]=None,
            blur_radius: Union[int, None]=None,
            blur_offset: Union[Tuple[int, int], None]=None,
            on_click: Union[Callable[..., None], None]=None,
        ) -> None:
        '''
        Initializes the CustomToolButton with the specified size, position, and arrow direction.
        
        Args:
            parent (QObject): The parent object for the button.
            size (Tuple[int, int]): The width and height of the button.
            pos (Tuple[int, int]): The X and Y position of the button.
            style_sheet (str): The stylesheet to apply to the button.
            is_right (bool): Whether the arrow should point to the right (True) or left (False).
            font (Union[QFont, None]): Optional font to apply to the button.
            blur_radius (Union[int, None]): Optional blur radius for the drop shadow effect.
            blur_offset (Union[Tuple[int, int], None]): Optional offset (x, y) for the drop shadow effect.
            on_click (Union[Callable[..., None], None]): Optional callback function for the button's clicked signal.
        '''
        super().__init__(parent)

        if is_right:
            self.setArrowType(Qt.RightArrow)
        else:
            self.setArrowType(Qt.LeftArrow)

        self.setFixedSize(*size)
        self.move(*pos)
        self.setStyleSheet(style_sheet)

        if font:
            self.setFont(font)
        
        if blur_radius and blur_offset:
            self.setGraphicsEffect(CustomDropShadow(blur_radius, blur_offset, QColor(63, 63, 63, 180))) # Semi-transparent shadow

        if on_click:
            self.clicked.connect(on_click)
