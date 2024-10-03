from src.utils.balance import get_future_monthly_balances, get_past_monthly_balances
from src.gui.widgets.label import CustomLabel, HeaderLabel, TrailLabel
from src.gui.widgets.buttons import CustomToolButton
from src.gui.widgets.graph import CustomGraphWidget
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
    see_graph_year_font,
)

from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import QObject

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from typing import List


class SeeGraphScreen(QWidget):
    '''
    SeeGraphScreen class represents the interface for displaying the balance graph along
    with the projection for future months.
    '''
    def __init__(self, parent: QObject) -> None:
        '''
        Initializes the SeeGraphScreen.

        Args:
            parent (QObject): The parent widget that provides context and functionality 
                for screen transitions.
        '''
        super().__init__()

        self.parent = parent
        
        self.current_date = datetime.now()

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
            text='Balance Graph',
            parent=self.screen_frame,
            geometry=(0, 100, 1045, 100),
            style_sheet=action_prompt_style_sheet,
            font=action_prompt_font
        )

        # Setting the graph widget
        CustomGraphWidget(
            parent=self.screen_frame,
            current_date=self.current_date,
            months=self.__get_surrounding_months(),
            values=self.__get_balance_values(),
            geometry=(120, 160, 850, 480),
            blur_radius=1,
            blur_offset=(1, 1)
        )

        # Setting the next date button
        CustomToolButton(
            parent=self.screen_frame,
            is_right=True,
            size=(35, 35),
            pos=(910, 175),
            style_sheet=tool_button_style_sheet,
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=lambda: self.__update_graph(next=True)
        )

        # Setting the prev date button
        CustomToolButton(
            parent=self.screen_frame,
            is_right=False,
            size=(35, 35),
            pos=(865, 175),
            style_sheet=tool_button_style_sheet,
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=lambda: self.__update_graph(next=False)
        )

        # Setting the year label
        CustomLabel(
            text=f'{self.current_date.year}',
            parent=self.screen_frame,
            geometry=(893, 220, 50, 30),
            style_sheet=action_prompt_style_sheet,
            font=see_graph_year_font
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

    def __get_balance_values(self) -> List[float]:
        '''
        Retrieve the balance values to be displayed in the graph.

        First, get the future projections for the next 6 months.
        Then, retrieve the past balance values for the previous 2 months.
        Concatenate those results to get the final balance list.

        Returns:
            List[float]: The balance values.
        '''
        # Get the balance 6 months from now
        _, last_day = calendar.monthrange(self.current_date.year, self.current_date.month)
        future_balance = get_future_monthly_balances(
            ledger=self.parent.manager.ledger,
            end_timestamp=self.current_date.replace(day=last_day) + relativedelta(months=6),
        )
        future_values_list = list(future_balance.values())

        # Get the balance 2 months past now
        past_balance = get_past_monthly_balances(
            ledger=self.parent.manager.ledger,
            end_timestamp=self.current_date.replace(day=1) - relativedelta(months=2),
        )
        past_values_list = list(past_balance.values())

        # Conditions when the user wants to change the displayed months
        if len(past_values_list) == 0:
            return future_values_list[-10:]
        if len(future_values_list) == 0:
            return past_values_list[::-1][:10]

        return past_values_list[::-1] + future_values_list
        
    def __get_surrounding_months(self) -> List[str]:
        '''
        Retrieve the x values of the graph. The months that the balances belong to.

        Returns:
            List[str]: The desired months.
        '''
        # Create a list of month abbreviations from Jan to Dec
        months = list(calendar.month_abbr)[1:]  # Skip the empty first element
        
        # Find the indices for the start month
        start_index = self.current_date.month - 1

        if start_index - 2 < 0:
            result = months[start_index - 2:] + months[0:start_index + 8]
        else:
            result = months[start_index - 2: start_index + 8]

        # Handle the wrap-around (i.e., if slicing goes beyond the end of the list)
        if len(result) < 10:
            result = result + months[:10 - len(result)]
        
        return result
    
    def __update_graph(self, next: bool) -> None:
        '''
        Updating the graph when the next or previous button is being pressed.
        Setting the curremt date accordingly and reloading the widgets.

        Returns:
            None.
        '''
        if next:
            _, last_day = calendar.monthrange(self.current_date.year, self.current_date.month)
            self.current_date = self.current_date.replace(day=last_day) + timedelta(1)
        else:
            self.current_date = self.current_date.replace(day=1) - timedelta(1)

        self.reload_widgets()

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
