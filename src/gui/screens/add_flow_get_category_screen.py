from src.gui.widgets.label import CustomLabel, HeaderLabel, TrailLabel
from src.gui.widgets.buttons import CustomPushButton, CustomToolButton
from src.gui.widgets.lists import CustomListSelection
from src.gui.widgets.logo import LogoLabel
from src.gui.widgets.progress_bar import ProgressBarLabel
from src.gui.utils.style_sheets import (
    tool_button_style_sheet,
    balance_increase_state_label_style_sheet,
    balance_decrease_state_label_style_sheet,
    balance_neutral_state_label_style_sheet,
    action_prompt_style_sheet,
    list_selection_style_sheet,
    buttons_style_sheet
)
from src.gui.utils.fonts import (
    action_prompt_font,
    list_selection_font,
    button_font
)

from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import QObject


class AddFlowGetCategoryScreen(QWidget):
    '''
    AddFlowGetCategoryScreen class represents the interface for getting the category
    of the transaction.
    '''
    def __init__(self, parent: QObject) -> None:
        '''
        Initializes the AddFlowGetCategoryScreen.

        Args:
            parent (QObject): The parent widget that provides context and functionality 
                for screen transitions.
        '''
        super().__init__()

        self.parent = parent

        # Placeholder for the available categories
        self.categories = []

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

        # Setting the action prompt label
        CustomLabel(
            text='Select the transaction category',
            parent=self.screen_frame,
            geometry=(10, 120, 1050, 100),
            style_sheet=action_prompt_style_sheet,
            font=action_prompt_font
        )

        # Setting the selection list
        self.list_selection = CustomListSelection(
            parent=self.screen_frame,
            items=self.categories,
            style_sheet=list_selection_style_sheet,
            geometry=(300, 200, 500, 300),
            font=list_selection_font,
            blur_radius=1,
            blur_offset=(1, 1)
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
            perc=25
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
        self.parent.fade_out_and_switch('add_flow_get_magnitude_screen')

    def next_button_pressed(self) -> None:
        '''
        Handles the event when the 'Next' button is pressed.

        Returns:
            None.
        '''
        # Get the selection widget
        selected_item = self.list_selection.currentItem()

        if selected_item:
            # Get the category text
            selected_text = selected_item.text()

            # Assign the category to the temporary flow
            self.parent.manager._flow.category = selected_text

            self.parent.fade_out_and_switch('add_flow_execution_screen')
        else:
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
