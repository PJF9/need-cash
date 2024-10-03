from src.gui.widgets.input_box import CustomInputBox
from src.gui.widgets.buttons import CustomPushButton
from src.gui.utils.style_sheets import (
    buttons_style_sheet,
    action_prompt_style_sheet,
    magnitude_input_box_style_sheet
)
from src.gui.utils.fonts import (
    execute_flows_action_label_font,
    execute_flow_input_box_font,
    execute_flow_buttons_font,
)

from PyQt5.QtWidgets import (
    QLabel,
    QDialog,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtGui import QFont, QDoubleValidator
from PyQt5.QtCore import QObject, Qt

from typing import Union


class CustomInfoWindow(QDialog):
    '''
    CustomInfoWindow is a borderless, transparent QDialog window designed to display a styled message label.
    This window can be customized in terms of text, styling, font, and position relative to a parent widget.
    '''
    def __init__(self,
            text: str,
            style_sheet: str,
            font: Union[QFont, None]=None,
            parent: Union[QObject, None]=None,
        ) -> None:
        '''
        Initializes the CustomInfoWindow with the specified text, style, and font.

        Args:
            text (str): The text to be displayed in the window.
            style_sheet (str): The CSS style sheet to style the label.
            font (Union[QFont, None]): An instance of QFont to customize the label's text font (default is None).
            parent (Union[QObject, None]): The parent widget for this window, allowing it to inherit properties
                such as modal behavior or stay-on-top properties (default is None).
        '''
        super().__init__(parent)
        
        # Set window flags to create a frameless window that stays on top of all other windows
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # Create a QLabel to display the provided text
        label = QLabel(text, self)

        # Apply the specified style sheet to the label
        label.setStyleSheet(style_sheet)
        
        # Apply margin to the label (specific inline margin settings)
        label.setStyleSheet('margin: 10px 0px 0px 0px')
        
        # Apply a default or provided font to the label
        if font:
            label.setFont(font)

        # Adjust the label size to fit the content
        label.adjustSize()
        
        # Adjust the size of the window to barely fit the label with a small padding
        self.setFixedSize(label.size().width() + 10, label.size().height() + 10)

        # Set the window opacity to 80%, making the window semi-transparent
        self.setWindowOpacity(0.8)


class FlowSizeInputDialog(QDialog):
    '''
    A custom dialog window that prompts the user to enter the real size of a flow. It contains an input field
    for the user to type in the flow size and two buttons ("Ok" and "Cancel") to confirm or cancel the input.
    '''
    def __init__(self,
            parent=None
        ) -> None:
        '''
        Initializes the FlowSizeInputDialog instance with the provided parent widget.

        Args:
            parent (QWidget, optional): The parent widget for this dialog (default is None).
        '''
        super().__init__(parent)
        
        self.setWindowTitle('Get Flow Size')
        self.setFixedSize(330, 185)  # Set a fixed size for the dialog
        
        # Create a label with a prompt message
        self.label = QLabel('Type the real size of the flow', self)
        self.label.setStyleSheet(action_prompt_style_sheet)
        self.label.setFont(execute_flows_action_label_font)
        self.label.setAlignment(Qt.AlignCenter)

        # Create an input field for entering the flow size
        self.input_field = CustomInputBox(
            parent=self,
            style_sheet=magnitude_input_box_style_sheet,
            geometry=(0, 0, 100, 100),
            validator=QDoubleValidator(0, 1e12, 2),
            font=execute_flow_input_box_font,
            blur_radius=1,
            blur_offset=(1,1)
        )
        
        # Create the "Ok" button to confirm the input
        self.ok_button = CustomPushButton(
            text='Ok',
            parent=self,
            size=(100, 50),
            pos=(0, 0),
            style_sheet=buttons_style_sheet,
            font=execute_flow_buttons_font,
            blur_radius=1,
            blur_offset=(1,1),
            on_click=self.accept
        )

        # Create the "Cancel" button to cancel the input
        self.cancel_button = CustomPushButton(
            text='Cancel',
            parent=self,
            size=(100, 50),
            pos=(0, 0),
            style_sheet=buttons_style_sheet,
            font=execute_flow_buttons_font,
            blur_radius=1,
            blur_offset=(1,1),
            on_click=self.reject
        )
        
        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        # Create the main layout for the dialog
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.input_field)
        main_layout.addLayout(button_layout)
        
        # Set the main layout as the layout for the dialog
        self.setLayout(main_layout)

    def get_input(self) -> None:
        '''
        Retrieves the text entered by the user in the input field.

        Returns:
            str: The text entered in the input field.
        '''
        return self.input_field.text()


class ConfirmDeleteDialog(QDialog):
    '''
    A custom dialog window that prompts the user to confirm the deletion of a flow. It displays a message
    asking for confirmation and provides two buttons ("Yes" and "No") for the user to confirm or cancel the
    deletion action.
    '''
    def __init__(self,
            parent=None
        ) -> None:
        '''
        Initializes the ConfirmDeleteDialog instance with the provided parent.

        Args:
            parent (QWidget, optional): The parent widget for this dialog (default is None).
        '''
        super().__init__(parent)
        
        self.setWindowTitle('Confirm Deletion')
        self.setFixedSize(465, 150)  # Set a fixed size for the dialog

        # Create a label with the confirmation message
        self.label = QLabel(f'Are you sure you want to delete this flow?', self)
        self.label.setStyleSheet(action_prompt_style_sheet)
        self.label.setFont(execute_flows_action_label_font)
        self.label.setAlignment(Qt.AlignCenter)

        # Create the "Yes" button to confirm deletion
        self.yes_button = CustomPushButton(
            text='Yes',
            parent=self,
            size=(100, 50),
            pos=(0, 0),
            style_sheet=buttons_style_sheet,
            font=execute_flow_buttons_font,
            blur_radius=1,
            blur_offset=(1,1),
            on_click=self.accept
        )

        # Create the "No" button to cancel deletion
        self.no_button = CustomPushButton(
            text='No',
            parent=self,
            size=(100, 50),
            pos=(0, 0),
            style_sheet=buttons_style_sheet,
            font=execute_flow_buttons_font,
            blur_radius=1,
            blur_offset=(1,1),
            on_click=self.reject
        )

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)

        # Create the main layout for the dialog
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addLayout(button_layout)

        # Set the main layout as the layout for the dialog
        self.setLayout(main_layout)
