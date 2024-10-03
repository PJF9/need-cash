from src.gui.screens.main_screen import MainScreen
from src.gui.screens.add_flow_get_magnitude_screen import AddFlowGetMagnitudeScreen
from src.gui.screens.add_flow_get_category_screen import AddFlowGetCategoryScreen
from src.gui.screens.add_flow_execution_screen import AddFlowExecutionScreen
from src.gui.screens.add_flow_get_reccurent_screen import AddFlowGetRecurentScreen
from src.gui.screens.add_flow_get_comment_screen import AddFlowGetCommentScreen
from src.gui.screens.see_flows_screen import SeeFlowsScreen
from src.gui.screens.edit_pending_flow_screen import EditPendingFlowsScreen
from src.gui.screens.see_graph_screen import SeeGraphScreen
from src.gui.app_manager import AppManager

from PyQt5.QtWidgets import (
    QWidget,
    QStackedWidget,
    QHBoxLayout
)
from PyQt5.QtCore import QPropertyAnimation


class NeedCashApp(QWidget):
    '''
    A main application window for the NeedCash application that manages and displays
    different screens through a QStackedWidget.

    This class serves as the container for multiple screens of the NeedCash app, such as 
    the main screen, various "add flow" screens, and other views like flow visualization 
    and graph viewing. It includes functionality for switching between these screens 
    and adding animations to transitions.

    Attributes:
        manager (AppManager): The application manager that controls the app's data flow.
        layout (QHBoxLayout): The main layout holding the stacked widget.
        stack (QStackedWidget): A widget to stack and switch between different screens.
        main_screen (MainScreen): The main screen of the application.
        add_flow_get_magnitude_screen (AddFlowGetMagnitudeScreen): Screen to input magnitude for a new flow.
        add_flow_get_category_screen (AddFlowGetCategoryScreen): Screen to choose a category for the flow.
        add_flow_execution_screen (AddFlowExecutionScreen): Screen to execute the flow process.
        add_flow_get_reccurent_screen (AddFlowGetRecurentScreen): Screen to set recurrent flow information.
        add_flow_get_comment_screen (AddFlowGetCommentScreen): Screen to add comments for the flow.
        see_flows_screen (SeeFlowsScreen): Screen to view the list of flows.
        edit_pending_flow_screen (EditPendingFlowsScreen): Screen to edit pending flows.
        see_graph_screen (SeeGraphScreen): Screen to view a graph of financial data.
    '''
    def __init__(self, manager: AppManager) -> None:
        '''
        Initializes the NeedCashApp by setting up the layout, the QStackedWidget, and
        adding all the necessary screens to the stack.

        Args:
            manager (AppManager): The manager that controls the overall application state.
        '''
        super().__init__()

        # Initialize the app manager
        self.manager = manager

        # Set window properties
        self.setWindowTitle('NeedCash')
        self.setGeometry(100, 100, 1100, 800)
        self.setStyleSheet('background-color: #ffffff;')

        # Create a layout that will hold the changing content
        self.layout = QHBoxLayout()

        # Use a QStackedWidget to hold multiple screens
        self.stack = QStackedWidget(self)

        # Initialize all the screens of the application
        self.main_screen = MainScreen(self)
        self.add_flow_get_magnitude_screen = AddFlowGetMagnitudeScreen(self)
        self.add_flow_get_category_screen = AddFlowGetCategoryScreen(self)
        self.add_flow_execution_screen = AddFlowExecutionScreen(self)
        self.add_flow_get_reccurent_screen = AddFlowGetRecurentScreen(self)
        self.add_flow_get_comment_screen = AddFlowGetCommentScreen(self)
        self.see_flows_screen = SeeFlowsScreen(self)
        self.edit_pending_flow_screen = EditPendingFlowsScreen(self)
        self.see_graph_screen = SeeGraphScreen(self)

        # Add screens to the QStackedWidget
        self.stack.addWidget(self.main_screen)                   # index 0
        self.stack.addWidget(self.add_flow_get_magnitude_screen) # index 1
        self.stack.addWidget(self.add_flow_get_category_screen)  # index 2
        self.stack.addWidget(self.add_flow_execution_screen)     # index 3
        self.stack.addWidget(self.add_flow_get_reccurent_screen) # index 4
        self.stack.addWidget(self.add_flow_get_comment_screen)   # index 5
        self.stack.addWidget(self.see_flows_screen)              # index 6
        self.stack.addWidget(self.edit_pending_flow_screen)      # index 7
        self.stack.addWidget(self.see_graph_screen)              # index 8

        # Add the stack to the layout
        self.layout.addWidget(self.stack)

        # Set the layout for the window
        self.setLayout(self.layout)

    def switch_to(self, screen_name: str) -> None:
        '''
        Switches the visible screen in the QStackedWidget based on the screen name.

        Args:
            screen_name (str): The name of the screen to switch to.
        
        Returns:
            None.
        '''
        if screen_name == 'main_screen':
            self.stack.setCurrentWidget(self.main_screen)  # Switch to main screen
        elif screen_name == 'add_flow_get_magnitude_screen':
            self.stack.setCurrentWidget(self.add_flow_get_magnitude_screen)  # Switch to add flow get magnitude screen
        elif screen_name == 'add_flow_get_category_screen':
            self.stack.setCurrentWidget(self.add_flow_get_category_screen) # Switch to add flow get category screen
        elif screen_name == 'add_flow_execution_screen':
            self.stack.setCurrentWidget(self.add_flow_execution_screen) # Switch to add flow execution screen
        elif screen_name == 'add_flow_get_recurrent_screen':
            self.stack.setCurrentWidget(self.add_flow_get_reccurent_screen) # Switch to add flow get recurrent screen
        elif screen_name == 'add_flow_get_comment_screen':
            self.stack.setCurrentWidget(self.add_flow_get_comment_screen) # Switch to add flow get comment screen
        elif screen_name == 'see_flows_screen':
            self.stack.setCurrentWidget(self.see_flows_screen) # Switch to the see flows screen
        elif screen_name == 'edit_pending_flows_screen':
            self.stack.setCurrentWidget(self.edit_pending_flow_screen) # Switch to edit flows screen
        elif screen_name == 'see_graph_screen':
            self.stack.setCurrentWidget(self.see_graph_screen) # Switch to the graph screen

    def fade_out_and_switch(self, screen_name: str) -> None:
        '''
        Fades out the current screen, switches to the new screen, and fades it back in.

        Args:
            screen_name (str): The name of the screen to switch to.
        
        Returns:
            None.
        '''
        self.fade_animation = QPropertyAnimation(self, b'windowOpacity')
        self.fade_animation.setDuration(200)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.finished.connect(lambda: self.switch_to(screen_name))
        self.fade_animation.finished.connect(self.fade_in)
        self.fade_animation.start()

    def fade_in(self) -> None:
        '''
        Fades in the currently visible screen after a switch.
        
        Returns:
            None.
        '''
        self.fade_animation = QPropertyAnimation(self, b'windowOpacity')
        self.fade_animation.setDuration(100)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()

    def reload_windows(self) -> None:
        '''
        Reloads all the windows and their widgets, ensuring the latest data is displayed.
        
        Returns:
            None.
        '''
        # Reload every window
        self.main_screen.reload_widgets()
        self.add_flow_get_magnitude_screen.reload_widgets()
        self.add_flow_get_category_screen.reload_widgets()
        self.add_flow_execution_screen.reload_widgets()
        self.add_flow_get_reccurent_screen.reload_widgets()
        self.add_flow_get_comment_screen.reload_widgets()
        self.see_flows_screen.reload_widgets()
        self.edit_pending_flow_screen.reload_widgets()
        self.see_graph_screen.reload_widgets()
