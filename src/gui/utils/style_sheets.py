balance_label_style_sheet = '''
    background-color: #fbfbfb;
    border-radius: 5px;
'''

balance_increase_state_label_style_sheet = '''
    background-color: #00FF00;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
'''
balance_decrease_state_label_style_sheet = '''
    background-color: #FF4747;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
'''
balance_neutral_state_label_style_sheet = '''
    background-color: #B8B8B8;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
'''

buttons_style_sheet = '''
    QPushButton {
        background-color: #fbfbfb;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #5dade2;
    }
    QPushButton:pressed {
        background-color: #2e86c1;
    }
'''

tool_button_style_sheet = '''
    QToolButton {
        background-color: #fbfbfb;
        border-radius: 10px;
        padding: 10px;
    }
    QToolButton:hover {
        background-color: #5dade2;
    }
    QToolButton:pressed {
        background-color: #2e86c1;
    }
'''

trail_style_sheet = '''
    background-color: white;
'''

action_prompt_style_sheet = '''
    background-color: white;
'''

magnitude_input_box_style_sheet = '''
    QLineEdit {
        background-color: #fbfbfb;
        border-radius: 5px;
        padding: 5px;
    }
    QLineEdit:focus {
        background-color: white
    }
'''

green_button_style_sheet = '''
    QPushButton {
        background-color: #00FF00;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #00E300;
    }
    QPushButton:pressed {
        background-color: #00CB00;
    }
'''

red_button_style_sheet = '''
    QPushButton {
        background-color: #FF4747;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #F13434;
    }
    QPushButton:pressed {
        background-color: #D72020;
    }
'''

progress_bar_placeholder_style_sheet = '''
    background-color: #B8B8B8;
    border-radius: 10px;
'''
progress_bar_style_sheet = '''
    background-color: #6300B1;
    border-radius: 10px;
'''
progress_bar_text_style_sheet = '''
    background-color: white;
    color: #6300B1 
'''

list_selection_style_sheet = '''
    QListWidget {
        background-color: white;
        border-radius: 10px;
        padding: 5px;
        margin: 10px;
    }

    QListWidget::item {
        background-color: #FFFFFF;
        color: black;
        padding: 10px;
        border: 1px solid #CCCCCC;
        margin: 5px;
        border-radius: 10px;
    }
                          
    QListWidget::item:hover {
        background-color: #D3D3D3;
    }
    
    QListWidget::item:selected {
        background-color: #A0A0A0;
        color: #FFFFFF;
        font-weight: bold;
        border: 1px solid 007AA3;
    }
                          
    QScrollBar:vertical {
        border: none;
        background: #D3D3D3;
        width: 15px;
        margin: 15px 0 15px 0;
    }

    QScrollBar::handle:vertical {
        background: #C3C3C3;
        min-height: 20px;
        border-radius: 7px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #667;
    }
                          
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
        height: 0px;
    }
'''

caledar_style_sheet = '''
    /* Main Calendar Background */
    QCalendarWidget QWidget {
        background-color: #FFFFFF;  /* White background */
        selection-background-color: transparent;
    }

    /* Navigation Buttons */
    QCalendarWidget QToolButton {
        color: black;                       /* Black text */
        background: transparent;            /* Transparent background */
        border: none;                       /* No border */
        font-size: 18px;                    /* Larger font for month/year */
        margin: 5px;                        /* Margin around buttons */
    }

    QCalendarWidget QToolButton#qt_calendar_prevmonth,
    QCalendarWidget QToolButton#qt_calendar_nextmonth {
        qproperty-iconSize: 20px;           /* Smaller arrow buttons */
        width: 25px;
        height: 25px;
    }

    QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
    QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
        background-color: #e8e8e8;          /* Light gray on hover */
        border-radius: 5px;                 /* Rounded hover effect */
    }

    /* Weekday Header */
    QCalendarWidget QHeaderView::section {
        background-color: white;            /* White background for header */
        color: black;                       /* Black text for day names */
        font-weight: bold;                  /* Bold text */
        padding: 5px;                       /* Padding around day names */
        border: none;                       /* No borders */
        font-size: 14px;                    /* Adjust font size */
    }

    /* Day Numbers */
    QCalendarWidget QAbstractItemView:enabled {
        color: black;                       /* Black text for all days */
        selection-background-color: #1A73E8;/* Blue for selected date */
        selection-color: white;             /* White text for selected date */
    }

    QCalendarWidget QAbstractItemView:disabled {
        color: #d3d3d3;                     /* Light gray for inactive days */
    }

    QCalendarWidget QAbstractItemView QTableView::item {
        padding: 10px;                      /* Padding for day numbers */
        border: none;                       /* No border */
    }

    QCalendarWidget QAbstractItemView::item:selected {
        background-color: #5dade2;          /* Blue background for selected date */
        color: white;                       /* White text for selected date */
        border-radius: 2px;                /* Rounded effect for selected date */
        margin: 2px;                        /* Margin to fit the rounded circle */
    }

    /* Today's Date */
    QCalendarWidget QAbstractItemView::item:!selected:enabled:today {
        background-color: #d1e7ff;          /* Light blue background for today */
        color: black;                       /* Black text */
        border-radius: 15px;                /* Rounded circle */
        border: none;                       /* Remove border for today's date */
    }
'''

confirm_flow_style_sheet = '''
    background-color: white;
    border-radius: 5px;
'''
confirm_inflow_style_sheet = '''
    background-color: #00FF00;
    border-top-left-radius: 0px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 5px;
'''
confirm_outflow_style_sheet = '''
    background-color: #FF4747;
    border-top-left-radius: 0px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 5px;
'''


scroll_bar_style_sheet = '''
    QScrollArea {
        border-left: none;  /* Border on the left side */
        border-bottom: 1px solid white; /* Border on the bottom side */
        border-top: none;  /* No border on the top */
        border-right: 1px solid white; /* No border on the right */
    }

    QScrollBar:vertical {
        background: white;         /* Background color of the scroll bar */
        width: 12px;                 /* Width of the scroll bar */
        margin: 2px;                 /* Margin around the scroll bar */
    }
    QScrollBar::handle:vertical {
        background: #A9A9A9;         /* Handle color */
        min-height: 10px;            /* Minimum height of the handle */
        border-radius: 4px;          /* Border radius of the handle */
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;                 /* Remove the arrows at the ends */
        background: none;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;            /* Transparent background between handle and end */
    }
    QScrollBar::handle:vertical:hover {
        background: #8E8E8E;        /* Handle color when hovered */
    }
    QScrollBar::handle:vertical:pressed {
        background: #747474;       /* Handle color when pressed */
    }
'''
