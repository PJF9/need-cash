from src.flow import Flow
from src.utils.save import save_ledger
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
    confirm_flow_style_sheet
)
from src.gui.utils.fonts import (
    action_prompt_font,
    magnitude_font,
    button_font,
    confirm_flow_font
)

from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import QObject

from datetime import datetime


class AddFlowGetCommentScreen(QWidget):
    '''
    AddFlowGetCommentScreen class represents the interface for adding some commends to the
    transaction, and confirming the final flow.
    '''
    def __init__(self, parent: QObject) -> None:
        '''
        Initializes the AddFlowGetCommentScreen.

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
            text='You can add additional comments about this transaction',
            parent=self.screen_frame,
            geometry=(10, 130, 1050, 100),
            style_sheet=action_prompt_style_sheet,
            font=action_prompt_font
        )

        # Setting the input box
        self.input_box = CustomInputBox(
            parent=self.screen_frame,
            style_sheet=magnitude_input_box_style_sheet,
            geometry=(130, 380, 800, 80),
            font=magnitude_font,
            max_length=100,
            blur_radius=3,
            blur_offset=(3, 3)
        )

        # Display temporary flow for confirmation
        self.flow_label = CustomLabel(
            text=f'',
            parent=self.screen_frame,
            geometry=(130, 230, 800, 90),
            style_sheet=confirm_flow_style_sheet,
            font=confirm_flow_font,
            blur_radius=2,
            blur_offset=(2, 2)
        )
        self.flow_state_label = CustomLabel(
            text='',
            parent=self.screen_frame,
            style_sheet='',
            geometry=(910, 230, 1, 1),
        )
        self.flow_state_label.setFixedHeight(90)
        self.flow_state_label.setFixedWidth(20)

        # Setting the submit button
        CustomPushButton(
            text='Submit Flow',
            parent=self.screen_frame,
            size=(205, 80),
            pos=(430, 530),
            style_sheet=buttons_style_sheet,
            font=button_font,
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=self.submit_button_pressed
        )

        # Setting the progress bar label
        ProgressBarLabel(
            parent=self.screen_frame,
            perc=100
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
        self.parent.fade_out_and_switch('add_flow_get_recurrent_screen')

    def submit_button_pressed(self) -> None:
        '''
        Handles the event when the 'Next' button is pressed.

        Returns:
            None.
        '''
        # Get the comments from the input box
        comments: str = self.input_box.text()

        # Initializing the flow that will be added to the ledger
        flow = Flow(
            size=self.parent.manager._flow.size,
            category=self.parent.manager._flow.category,
            time_executed=self.parent.manager._flow.time_executed,
            recurrent=self.parent.manager._flow.recurrent,
            comments=comments
        )

        if flow.time_executed.date() <= datetime.now().date():
            # Executed flow
            self.parent.manager.ledger.add_flow(flow, is_proj=False)
        
        if flow.time_executed.date() > datetime.now().date() or flow.recurrent != 0:
            # Projected flow
            self.parent.manager.ledger.add_flow(flow.copy(), is_proj=True)

        # Reset the app manager's flow
        self.parent.manager._flow.clear()

        # Save the updated ledger
        save_ledger(self.parent.manager.ledger, save_path=self.parent.manager.path)

        # Relaod all windows to add the new flow
        self.parent.reload_windows()

        # Switch to the next screen        
        self.parent.fade_out_and_switch('main_screen')

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
