from src.gui.widgets.label import CustomLabel, TrailLabel
from src.gui.widgets.buttons import CustomPushButton, CustomToolButton
from src.gui.widgets.notifications import CustomNotificationsDisplay
from src.gui.widgets.logo import LogoLabel

from src.gui.utils.style_sheets import (
    balance_label_style_sheet,
    balance_increase_state_label_style_sheet,
    balance_decrease_state_label_style_sheet,
    balance_neutral_state_label_style_sheet,
    buttons_style_sheet,
    tool_button_style_sheet,
)
from src.gui.utils.fonts import (
    balance_font,
    button_font,
)

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
)
from PyQt5.QtCore import QObject


class MainScreen(QWidget):
    '''
    MainScreen class represents the main user interface of the application.

    It displays the balance, allows the user to add flows, 
    and provides navigation to other screens.
    '''
    def __init__(self, parent: QObject) -> None:
        '''
        Initializes the MainScreen.

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
        Initializes the user interface components of the MainScreen.
        This includes setting up labels, buttons, and any other UI elements.

        Returns:
            None.
        '''
        # Setting up the logo label
        LogoLabel(
            parent=self.screen_frame,
            path='src/gui/assets/needcash_logo_tr.png',
            size=(320, 100),
            padding=(0, 0, 0, 0)
        )

        # Setting the Notification display
        CustomNotificationsDisplay(
            parent=self.screen_frame,
            flows=self.parent.manager.get_to_be_executed_flows()
        )

        # Setting up the balance
        CustomLabel(
            text=f'Balance: ${self.parent.manager.get_n_balance():.2f}',
            parent=self.screen_frame,
            style_sheet=balance_label_style_sheet,
            geometry=(300, 260, 450, 150),
            font=balance_font,
            blur_radius=5,
            blur_offset=(5, 5)
        )

        # Setting up the balance state label
        balance_state_label = CustomLabel(
            text='',
            parent=self.screen_frame,
            style_sheet=self.__get_balance_state_style_sheet(),
            geometry=(300, 395, 450, 1),
        )
        balance_state_label.setFixedHeight(15)

        # Setting up the add flow button
        CustomPushButton(
            text='Add Flow',
            parent=self.screen_frame,
            font=button_font,
            size=(205, 80),
            style_sheet=buttons_style_sheet,
            pos=(210, 550),
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=self.switch_to_add_flow_screen
        )

        # Setting up the see flows button
        CustomPushButton(
            text='See Flows',
            parent=self.screen_frame,
            font=button_font,
            size=(205, 80),
            style_sheet=buttons_style_sheet,
            pos=(610, 550),
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=self.switch_to_see_flows_screen
        )

        # Setting u[ the right arrow button
        CustomToolButton(
            parent=self.screen_frame,
            is_right=True,
            size=(60, 60),
            pos=(970, 325),
            style_sheet=tool_button_style_sheet,
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=self.switch_to_see_graph_screen
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

    def switch_to_add_flow_screen(self) -> None:
        '''
        Switches the display to the add flow screen.

        Returns:
            None.        
        '''
        self.parent.fade_out_and_switch('add_flow_get_magnitude_screen')

    def switch_to_see_flows_screen(self) -> None:
        '''
        Switches the display to the see flows screen.

        Returns:
            None.
        '''
        self.parent.fade_out_and_switch('see_flows_screen')

    def switch_to_see_graph_screen(self) -> None:
        '''
        Switches the display to the see graph screen.

        Returns:
            None.
        '''
        self.parent.fade_out_and_switch('see_graph_screen')

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
