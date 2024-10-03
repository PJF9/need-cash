from src.gui.widgets.label import CustomLabel, HeaderLabel, TrailLabel
from src.gui.widgets.buttons import CustomToolButton
from src.gui.widgets.lists import CustomEditListDisplay
from src.gui.widgets.logo import LogoLabel

from src.gui.utils.style_sheets import (
    balance_increase_state_label_style_sheet,
    balance_decrease_state_label_style_sheet,
    balance_neutral_state_label_style_sheet,
    tool_button_style_sheet,
    action_prompt_style_sheet,
)
from src.gui.utils.fonts import (
    action_prompt_font,
    see_flows_field_font,
    see_flows_grid_font,
)

from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import QObject


class EditPendingFlowsScreen(QWidget):
    '''
    EditPendingFlowsScreen class represents the interface for editting the projected flows from the ledger.
    '''
    def __init__(self, parent: QObject) -> None:
        '''
        Initializes the EditPendingFlowsScreen.

        Args:
            parent (QObject): The parent widget that provides context and functionality 
                for screen transitions.
        '''
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

        # Setting the title label
        CustomLabel(
            text='Pending Flows',
            parent=self.screen_frame,
            geometry=(0, 100, 1055, 100),
            style_sheet=action_prompt_style_sheet,
            font=action_prompt_font
        )

        # Setting the list display
        CustomEditListDisplay(
            parent=self.screen_frame,
            main_app_instance=self.parent,
            geometry=(110, 190, 835, 420),
            field_font=see_flows_field_font,
            style_sheet='background-color: white;',
            grid_font=see_flows_grid_font,
            blur_radius=1,
            blur_offset=(1, 1)
        )

        # Setting the go back button
        CustomToolButton(
            parent=self.screen_frame,
            is_right=False,
            size=(60, 60),
            pos=(30, 325),
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
        self.parent.fade_out_and_switch('see_flows_screen')

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
