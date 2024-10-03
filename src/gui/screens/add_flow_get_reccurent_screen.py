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
    buttons_style_sheet,
    tool_button_style_sheet,
    confirm_inflow_style_sheet,
    confirm_outflow_style_sheet
)
from src.gui.utils.fonts import (
    action_prompt_font,
    magnitude_font,
    button_font,
    optional_font
)

from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QObject


class AddFlowGetRecurentScreen(QWidget):
    '''
    AddFlowGetRecurentScreen class represents the interface for getting the recurrent nature
    of the transaction. Usefull for creating the projections graph.
    '''
    def __init__(self, parent: QObject) -> None:
        '''
        Initializes the AddFlowGetRecurentScreen.

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

    def initUI(self):
        '''
        Initializes the user interface components.

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
            text='How often does this transaction recur (in days)?',
            parent=self.screen_frame,
            geometry=(10, 120, 1050, 100),
            style_sheet=action_prompt_style_sheet,
            font=action_prompt_font
        )
        # Setting the optional label
        CustomLabel(
            text='(Optional)',
            parent=self.screen_frame,
            geometry=(160, 310, 200, 90),
            style_sheet=action_prompt_style_sheet,
            font=optional_font
        )

        # Setting the input box
        self.input_box = CustomInputBox(
            parent=self.screen_frame,
            style_sheet=magnitude_input_box_style_sheet,
            geometry=(350, 310, 350, 80),
            font=magnitude_font,
            max_length=3,
            validator=QIntValidator(0, 365),
            blur_radius=3,
            blur_offset=(3, 3)
        )

        # Setting the next button
        CustomPushButton(
            text='Next',
            parent=self.screen_frame,
            size=(205, 80),
            pos=(430, 530),
            style_sheet=buttons_style_sheet,
            font=button_font,
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=self.next_button_pressed
        )

        # Setting the progress bar label
        ProgressBarLabel(
            parent=self.screen_frame,
            perc=75
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

        Returns:
            None.        
        '''
        self.parent.fade_out_and_switch('add_flow_execution_screen')

    def next_button_pressed(self) -> None:
        '''
        Handles the event when the 'Next' button is pressed.

        Returns:
            None.
        '''
        # Get the recurrent level from the user input
        recurrent: str = self.input_box.text()

        # Check if the input is empty
        if recurrent == '':
            self.parent.manager._flow.recurrent = 0
        else:
            self.parent.manager._flow.recurrent = int(recurrent)

        # Update the text label for the confirmation screen
        if self.parent.manager._flow.recurrent != 0:
            str_flow = f'Your Flow: {self.parent.manager._flow.size}\n({self.parent.manager._flow.category}, on {self.parent.manager._flow.time_executed.date()}, every {self.parent.manager._flow.recurrent} days)'
        else:
            str_flow = f'Your Flow: {self.parent.manager._flow.size}\n({self.parent.manager._flow.category}, on {self.parent.manager._flow.time_executed.date()})'
        self.parent.add_flow_get_comment_screen.flow_label.setText(str_flow)

        # Update the flow state on the confirmation screen
        if self.parent.manager._flow.size > 0:
            self.parent.add_flow_get_comment_screen.flow_state_label.setStyleSheet(confirm_inflow_style_sheet)
        else:
             self.parent.add_flow_get_comment_screen.flow_state_label.setStyleSheet(confirm_outflow_style_sheet)

        # Switch to the next screen        
        self.parent.fade_out_and_switch('add_flow_get_comment_screen')

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
