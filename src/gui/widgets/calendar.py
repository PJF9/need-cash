from src.gui.widgets.shadow import CustomDropShadow

from PyQt5.QtWidgets import QCalendarWidget, QWidget
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QIcon
from PyQt5.QtCore import Qt, QLocale, QDate 

from typing import Union, Tuple


class CustomCalendar(QCalendarWidget):
    '''
    CustomCalendar is a subclass of QCalendarWidget that provides a 
    tailored calendar experience with customizable styles, navigation 
    icons, date formats, and visual settings.
    '''
    def __init__(self,
            parent: QWidget,
            style_sheet: str,
            geometry: Tuple[int, int, int, int],
            font: Union[QFont, None] = None,
            blur_radius: Union[int, None] = None,
            blur_offset: Union[Tuple[int, int], None] = None
        ) -> None:
        '''
        Initializes a new instance of the CustomCalendar class.

        Args:
            parent (QWidget): The parent widget for this calendar.
            style_sheet (str): The stylesheet to apply to the calendar.
            geometry (Tuple[int, int, int, int]): The geometry (x, y, width, height) for the calendar.
            font (Union[QFont, None], optional): A QFont object to set the font of the calendar. Defaults to None.
            blur_radius (Union[int, None], optional): The blur radius for the shadow effect. Defaults to None.
            blur_offset (Union[Tuple[int, int], None], optional): The offset for the shadow effect as (x, y). Defaults to None.

        Initializes the calendar with the following settings:
        - Hides the grid and makes the navigation bar visible.
        - Sets the first day of the week to Monday.
        - Configures the locale to English (UK).
        - Adjusts header formats and sets a date range from 2000-01-01 to 2100-12-31.
        - Selects the current date and applies custom formatting for the header and weekend dates.
        - Changes the appearance of today's date with custom colors.
        - Applies a provided stylesheet and custom icons for navigation buttons.
        - Sets geometry and applies an optional font and blur effect.
        '''
        super().__init__(parent)

        # Hide grid
        self.setGridVisible(False)

        # Make navifation bar visable
        self.setNavigationBarVisible(True)

        # Remove the focus policy to remove the border from the selected category
        self.setFocusPolicy(Qt.NoFocus)

        # Set first day of the week to Monday
        self.setFirstDayOfWeek(Qt.Monday)

        # Set the Locale to English
        self.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

        # Adjusting header formats
        self.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        # Setting date range
        self.setMinimumDate(QDate(2000, 1, 1))
        self.setMaximumDate(QDate(2100, 12, 31))

        # Select current date
        self.setSelectedDate(QDate.currentDate())

        # Set the header text format
        header_format = QTextCharFormat()
        header_format.setFontWeight(2)  # Bold text
        header_format.setForeground(QColor('black'))
        header_format.setBackground(QColor('white'))
        self.setHeaderTextFormat(header_format)

        # Set weekends text format
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QColor('black'))  # Set to black color

        # Set formats for Saturday and Sunday
        self.setWeekdayTextFormat(6, weekend_format)  # Saturday
        self.setWeekdayTextFormat(7, weekend_format)  # Sunday

        # Change today's date colour
        today = QDate.currentDate()
        today_format = QTextCharFormat()
        today_format.setForeground(QColor('white'))
        today_format.setBackground(QColor('#6300B1'))
        self.setDateTextFormat(today, today_format)

        self.setStyleSheet(style_sheet)

        # Set custom icons for the navigation buttons
        self.findChild(QWidget, 'qt_calendar_prevmonth').setIcon(QIcon('./src/gui/assets/calendar_prev_month_button.png'))
        self.findChild(QWidget, 'qt_calendar_nextmonth').setIcon(QIcon('./src/gui/assets/calendar_next_month_button.png'))

        self.setGeometry(*geometry)

        if font:
            self.setFont(font)

        if blur_radius and blur_offset:
            self.setGraphicsEffect(CustomDropShadow(blur_radius, blur_offset))
