from src.gui.widgets.label import CustomLabel, HeaderLabel, TrailLabel
from src.gui.widgets.buttons import CustomPushButton, CustomToolButton
from src.gui.widgets.input_box import CustomInputBox
from src.gui.widgets.logo import LogoLabel
from src.gui.widgets.progress_bar import ProgressBarLabel
from src.gui.utils.style_sheets import (
    balance_increase_state_label_style_sheet,
    balance_decrease_state_label_style_sheet,
    balance_neutral_state_label_style_sheet,
    action_prompt_style_sheet,
    magnitude_input_box_style_sheet,
    green_button_style_sheet,
    red_button_style_sheet,
    tool_button_style_sheet
)
from src.gui.utils.fonts import (
    action_prompt_font,
    magnitude_font,
    button_font,
)

from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QObject


class AddFlowGetMagnitudeScreen(QWidget):
    '''
    AddFlowGetMagnitudeScreen class represents the interface for getting the magnitude of a flow,
    when the add flow button has being pressed.
    '''
    def __init__(self, parent: QObject) -> None:
        '''
        Initializes the AddFlowGetMagnitudeScreen.

        Args:
            parent (QObject): The parent widget that provides context and functionality 
                for screen transitions.
        '''
        super().__init__()

        self.parent = parent  # Reference to the parent widget to switch screens

        super().__init__()

        self.parent = parent

        # The screen layout
        self.layout = QVBoxLayout()

        # The frame in which all widgets will be placed
        self.screen_frame = QFrame(self)

        # Initialize the UI with the custom widgets
        self.initUI()

        # Add the frame to the layout
        self.layout.addWidget(self.screen_frame)

        self.setLayout(self.layout)

    def initUI(self) -> None:
        '''
        Initializes the user interface components of the first add flow screen.
        This includes setting up labels, buttons, and any other UI elements.

        Returns:
            None.
        '''
        # Setting up the logo label
        LogoLabel(
            parent=self.screen_frame,
            path='src/gui/assets/needcash_logo_tr.png',
            size=(300, 80),
            padding=(0, 0, 0, 0)
        )

        # Setting the header balance label
        HeaderLabel(
            parent=self.screen_frame,
            state_style_sheet=self.__get_balance_state_style_sheet(),
            balance=self.parent.manager.get_n_balance()
        )

        # Setting the action prompt label
        CustomLabel(
            text='Enter the transaction amount',
            parent=self.screen_frame,
            geometry=(10, 120, 1050, 100),
            style_sheet=action_prompt_style_sheet,
            font=action_prompt_font
        )

        # Setting the input box
        self.input_box = CustomInputBox(
            parent=self.screen_frame,
            style_sheet=magnitude_input_box_style_sheet,
            geometry=(350, 250, 350, 80),
            font=magnitude_font,
            max_length=15,
            validator=QDoubleValidator(0, 1e12, 2),
            blur_radius=3,
            blur_offset=(3, 3)
        )

        # Setting the inflow button
        CustomPushButton(
            text='Infow',
            parent=self.screen_frame,
            size=(180, 80),
            pos=(285, 450),
            style_sheet=green_button_style_sheet,
            font=button_font,
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=self.inflow_button_pressed
        )

        # Setting the outflow button
        CustomPushButton(
            text='Outflow',
            parent=self.screen_frame,
            size=(180, 80),
            pos=(585, 450),
            style_sheet=red_button_style_sheet,
            font=button_font,
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=self.outflow_button_pressed
        )

        # Setting the progress bar label
        ProgressBarLabel(
            parent=self.screen_frame,
            perc=0
        )

        # Setting the go back button
        CustomToolButton(
            parent=self.screen_frame,
            is_right=False,
            size=(60, 60),
            pos=(40, 325),
            style_sheet=tool_button_style_sheet,
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=self.back_button_pressed
        )

        # Setting up the trail label
        TrailLabel(
            parent=self.screen_frame,
            account_name=self.parent.manager.get_account_name(),
            n_flows=self.parent.manager.get_n_flows(),
            n_projections=self.parent.manager.get_n_projections()
        )

    def __clear_layout(self) -> None:
        '''
        Remove all widgets from the layout.
        
        Returns:
            None.
        '''
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def __set_flow_magnitude(self, sign: int) -> bool:
        '''
        Sets the flow magnitude based on user input and assigns it to a temporary flow attribute.

        This method retrieves the magnitude value entered by the user from a QLineEdit input box (`self.input_box`),
        converts it to a float, applies the specified `sign`, and assigns the calculated value to the
        flow's `size` attribute. If no input is provided, it triggers a screen transition.

        Args:
            sign (int): The sign of the magnitude, typically `1` for positive and `-1` for negative,
                which determines the direction of the flow.

        Returns:
            (bool): 
                - `True` if the magnitude was successfully retrieved, converted, and assigned.
                - `False` if the input box was empty, indicating that the process could not proceed.
        '''
        # Get the magnitude from the user input
        magnitude: str = self.input_box.text()

        # Check if the input is empty
        if magnitude == '':
            # Transition to the 'add_flow_get_magnitude_screen' if no input is provided
            self.parent.fade_out_and_switch('add_flow_get_magnitude_screen')
            return False

        # Convert the magnitude from str to float, handling decimal separators (',' -> '.')
        size = float(magnitude.replace(',', '.'))

        # Assign the computed flow size to the temporary flow, applying the sign
        self.parent.manager._flow.size = size * sign

        return True

    def __get_balance_state_style_sheet(self) -> str:
        '''
        Get the style sheet of the balance label based on its state.

        Returns:
            str: The style sheet
        '''
        # Determing the state of the account
        state = self.parent.manager.get_state_balance()
        if state == 1:
            return balance_increase_state_label_style_sheet
        elif state == -1:
            return balance_decrease_state_label_style_sheet
        return balance_neutral_state_label_style_sheet

    def back_button_pressed(self) -> None:
        '''
        Handles the event when the 'Back' button is pressed.

        This method triggers a transition back to the 'main_screen' by calling the `fade_out_and_switch`
        method on the parent widget, effectively returning the user to the main screen of the application.

        Returns:
            None.
        '''
        self.parent.fade_out_and_switch('main_screen')

    def inflow_button_pressed(self) -> None:
        '''
        Handles the event when the 'Inflow' button is pressed.

        Returns:
            None.
        '''
        # Display only the inflow categories on the next screen
        self.parent.add_flow_get_category_screen.categories = [
            'Salary',
            'Contract Work',
            'Investment',
            'Interest',
            'Other'
        ]
        self.parent.add_flow_get_category_screen.reload_widgets()

        if self.__set_flow_magnitude(1):
            self.parent.fade_out_and_switch('add_flow_get_category_screen')

    def outflow_button_pressed(self) -> None:
        '''
        Handles the event when the 'Outflow' button is pressed.

        Returns:
            None.
        '''
        # Display only the outflow categories on the next screen
        self.parent.add_flow_get_category_screen.categories = [
            'Fixed Expense',
            'Groceries',
            'Going Out',
            'Entertainment',
            'Utility Bill',
            'Transportation',
            'Healthcare',
            'Education',
            'Clothing',
            'Personal Care',
            'Other'
        ]
        self.parent.add_flow_get_category_screen.reload_widgets()

        if self.__set_flow_magnitude(-1):
            self.parent.fade_out_and_switch('add_flow_get_category_screen')

    def reload_widgets(self) -> None:
        '''
        Reload all widgets.
        
        Returns:
            None.
        '''
        # Clear the layout (delete all widgets from it)
        self.__clear_layout()
        
        # Relaod the frame that will be added to the layout
        self.screen_frame = QFrame(self)

        # Initialize once again all the widgets within the frame
        self.initUI()

        # Add the new frame to the layout
        self.layout.addWidget(self.screen_frame)
