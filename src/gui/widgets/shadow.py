from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from typing import Union, Tuple


class CustomDropShadow(QGraphicsDropShadowEffect):
    '''
    A custom drop shadow effect for widgets with configurable blur radius, offset, and color.
    '''
    def __init__(self,
            blur_radius: int,
            blur_offset: Tuple[int, int],
            color: Union[QColor, None]=None
        ) -> None:
        '''
        Initializes the CustomDropShadow with the specified blur radius, offset, and optional color.

        Args:
            blur_radius (int): The blur radius for the shadow.
            blur_offset (Tuple[int, int]): The X and Y offsets for the shadow.
            color (Union[QColor, None]): The color of the shadow. If None, defaults to the default shadow color.
        '''
        super().__init__()

        self.setBlurRadius(blur_radius)
        self.setOffset(*blur_offset)

        if color:
            self.setColor(color)
