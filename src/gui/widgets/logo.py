from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject

from typing import Tuple


class LogoLabel(QLabel):
    '''
    A custom QLabel widget for displaying a logo image with a fixed size and padding.
    '''
    def __init__(self,
            parent: QObject,
            path: str,
            size: Tuple[int, int],
            padding: Tuple[int, int, int, int]
        ) -> None:
        '''
        Initializes the LogoLabel with a given image, size, and padding.

        Args:
            parent (QObject): The parent object for the label.
            path (str): The file path to the logo image.
            size (Tuple[int, int]): The fixed width and height of the logo.
            padding (Tuple[int, int, int, int]): The content margins (left, top, right, bottom) for the logo.
        '''
        super().__init__(parent)
        self.setPixmap(QPixmap(path))
        self.setFixedSize(*size)
        self.setScaledContents(True)
        self.setContentsMargins(*padding)
