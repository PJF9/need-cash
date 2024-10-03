from src.flow import Flow
from src.gui.widgets.shadow import CustomDropShadow
from src.gui.widgets.label import CustomLabel
from src.gui.widgets.action_buttons import ExecuteFlowButton, DeleteFlowButton
from src.gui.utils.style_sheets import (
    scroll_bar_style_sheet,
    green_button_style_sheet,
    red_button_style_sheet,
)

from PyQt5.QtWidgets import (
    QListWidget, 
    QListWidgetItem,
    QLabel,
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QGridLayout,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QObject, Qt

from datetime import datetime, timedelta
from typing import Union, List, Tuple, Iterable


class CustomListSelection(QListWidget):
    '''
    A custom list selection widget that extends QListWidget. This widget is designed 
    to display a list of items with customizable appearance and behavior, such as 
    alignment, style, and graphics effects.
    '''
    def __init__(self,
            parent: QObject,
            items: List[str],
            style_sheet: str,
            geometry: Tuple[int, int, int, int],
            font: Union[QFont, None] = None,
            blur_radius: Union[int, None] = None,
            blur_offset: Union[Tuple[int, int], None] = None
        ) -> None:
        '''
        Initializes a CustomListSelection widget.

        Args:
            parent (QObject): The parent object for this widget.
            items (List[str]): A list of items to add to the selection list.
            style_sheet (str): The stylesheet to apply to the widget for customization.
            geometry (Tuple[int, int, int, int]): The geometry of the widget specified as 
                (x, y, width, height).
            font (Union[QFont, None], optional): The font to set for the widget. Defaults to None.
            blur_radius (Union[int, None], optional): The radius of the blur effect for 
                the drop shadow. Defaults to None.
            blur_offset (Union[Tuple[int, int], None], optional): The x and y offset for the 
                drop shadow effect. Defaults to None.
        '''
        super().__init__(parent)
        self.setItemAlignment(Qt.AlignCenter)

        # Add the given items to the selection list
        self.__add_items(items)

        # Remove the focus policy to remove the border from the selected category
        self.setFocusPolicy(Qt.NoFocus)

        self.setStyleSheet(style_sheet)

        self.setGeometry(*geometry)

        if font:
            self.setFont(font)

        if blur_radius and blur_offset:
            self.setGraphicsEffect(CustomDropShadow(blur_radius, blur_offset))

    def __add_items(self, items: List[str]) -> None:
        '''
        Private method to add items to the QListWidget.

        This method iterates through the provided list of items and adds each 
        item as a QListWidgetItem to the widget.

        Args:
            items (List[str]): A list of strings representing the items to be added 
                to the list widget.
        '''
        for item_str in items:
            item_widget = QListWidgetItem(item_str)  # Create a QListWidgetItem
            item_widget.setTextAlignment(Qt.AlignCenter) # Center align the text
            self.addItem(item_widget)  # Add the item to the list widget


class CustomListDisplay(QWidget):
    '''
    CustomListDisplay is a QWidget-based class that displays a scrollable, tabular list of flows, with each row containing 
    details about a specific flow such as its ID, size, category, execution time, recurrence, and state.
    The display includes support for custom fonts, drop shadow effects, and hoverable status indicators.
    '''
    def __init__(self,
            parent: QWidget,
            flows: Iterable[Flow],
            style_sheet: str,
            geometry: Tuple[int, int, int, int],
            field_font: Union[QFont, None] = None,
            grid_font: Union[QFont, None] = None,
            blur_radius: Union[int, None] = None,
            blur_offset: Union[Tuple[int, int], None] = None
        ) -> None:
        '''
        Initializes the CustomListDisplay with the given parameters to create a scrollable table-like display of flows.

        Args:
            parent (QWidget): The parent widget for this display.
            flows (Iterable[Flow]): An iterable of Flow objects containing the data to be displayed.
            style_sheet (str): The CSS style sheet for styling the CustomListDisplay widget.
            geometry (Tuple[int, int, int, int]): The geometry (x, y, width, height) of the widget.
            field_font (Union[QFont, None], optional): The font to apply to the field labels (default is None).
            grid_font (Union[QFont, None], optional): The font to apply to the grid cells (default is None).
            blur_radius (Union[int, None], optional): The blur radius for the drop shadow effect (default is None).
            blur_offset (Union[Tuple[int, int], None], optional): The (x, y) offset for the drop shadow effect (default is None).
        '''
        super().__init__(parent)

        # Create a QVBoxLayout to contain the scroll area
        main_layout = QVBoxLayout(self)

        # Create a QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its contents
        main_layout.addWidget(scroll_area)

        # Customize the QScrollArea's scroll bar style
        scroll_area.setStyleSheet(scroll_bar_style_sheet)

        # Create a container widget to hold the grid layout
        container_widget = QWidget()
        scroll_area.setWidget(container_widget)

        # Create the grid layout
        grid_layout = QGridLayout(container_widget)

        # Set the spacing between widgets
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(10, 10, 10, 10)  # Set left, top, right, bottom margins

        # Create the header labels for each column
        id_field_label = QLabel('Flow Id')
        size_field_label = QLabel('Size')
        category_field_label = QLabel('Category')
        time_executed_field_label = QLabel('Time Executed')
        recurrent_field_label = QLabel('Recurrent')
        state_field_label = QLabel('State')

        if field_font:
            id_field_label.setFont(field_font)
            size_field_label.setFont(field_font)
            category_field_label.setFont(field_font)
            time_executed_field_label.setFont(field_font)
            recurrent_field_label.setFont(field_font)
            state_field_label.setFont(field_font)

        # Add the field labels to the grid layout
        grid_layout.addWidget(id_field_label, 0, 0, alignment=Qt.AlignCenter)
        grid_layout.addWidget(size_field_label, 0, 1, alignment=Qt.AlignCenter)
        grid_layout.addWidget(category_field_label, 0, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(time_executed_field_label, 0, 3, alignment=Qt.AlignCenter)
        grid_layout.addWidget(recurrent_field_label, 0, 4, alignment=Qt.AlignCenter)
        grid_layout.addWidget(state_field_label, 0, 5, alignment=Qt.AlignCenter)

        # Sort the flows so the latest ones will be displayed first
        flows = sorted(flows, key=lambda f: f.time_executed, reverse=True)

        # Populate the grid with flow data
        for i, flow in enumerate(flows, start=1):
            padding_style_sheet = 'padding: 5px 0px,5px 0px;'

            # Create labels for each field in the flow and apply styles
            id_label = QLabel(str(flow.flow_id))
            id_label.setStyleSheet(padding_style_sheet)
            size_label = QLabel(str(flow.size))
            size_label.setStyleSheet(padding_style_sheet)
            category_label = QLabel(str(flow.category))
            category_label.setStyleSheet(padding_style_sheet)
            time_executed_label = QLabel(str(flow.time_executed.date()))
            time_executed_label.setStyleSheet(padding_style_sheet)
            recurrent_label = QLabel(str(flow.recurrent))
            recurrent_label.setStyleSheet(padding_style_sheet)

            if grid_font:
                id_label.setFont(grid_font)
                size_label.setFont(grid_font)
                category_label.setFont(grid_font)
                time_executed_label.setFont(grid_font)
                recurrent_label.setFont(grid_font)
            
            # Add the labels to the grid layout
            grid_layout.addWidget(id_label, 2*i, 0, alignment=Qt.AlignCenter)
            grid_layout.addWidget(size_label, 2*i, 1, alignment=Qt.AlignCenter)
            grid_layout.addWidget(category_label, 2*i, 2, alignment=Qt.AlignCenter)
            grid_layout.addWidget(time_executed_label, 2*i, 3, alignment=Qt.AlignCenter)
            grid_layout.addWidget(recurrent_label, 2*i, 4, alignment=Qt.AlignCenter)
            
            # Determine the status style sheet based on flow size
            if flow.size > 0:
                status_style_sheet = 'background-color: green; border-radius: 5px; margin: 5px 0px 5px 0px;'
            else:
                status_style_sheet = 'background-color: red; border-radius: 5px; margin: 5px 0px 5px 0px;'
            
            # Create a CustomLabel as a status indicator (on hover show comments)
            status_label = CustomLabel(
                text='',
                parent=None,
                geometry=(0, 0, 50, 10),
                style_sheet=status_style_sheet,
                hover_text=flow.comments,
                hover_style_sheet='color: black;'
            )
            status_label.setFixedHeight(50)
            status_label.setFixedWidth(10)

            # Add the status label to the grid layout
            grid_layout.addWidget(status_label, 2*i, 5, Qt.AlignCenter)

            # Add shadow separators between rows, except the last one
            if i < len(flows):
                shadow_label = QLabel('')
                shadow_label.setFixedHeight(1)
                shadow_label.setGraphicsEffect(CustomDropShadow(4, (0, 4)))

                # Add the shadow separator to the grid
                grid_layout.addWidget(shadow_label, 2*i + 1, 0, 1, 6)  # Span across all columns

        # Set the layout for the container widget
        container_widget.setLayout(grid_layout)

        self.setStyleSheet(style_sheet)
        self.setGeometry(*geometry)

        if blur_radius and blur_offset:
            self.setGraphicsEffect(CustomDropShadow(blur_radius, blur_offset))



class CustomEditListDisplay(QWidget):
    '''
    A custom widget that displays a scrollable, editable table-like view of projected flows from a ledger.
    This class allows users to view, execute, or delete specific flows in a visually organized grid layout.
    '''
    def __init__(self,
            parent: QWidget,
            main_app_instance: QObject,
            style_sheet: str,
            geometry: Tuple[int, int, int, int],
            field_font: Union[QFont, None] = None,
            grid_font: Union[QFont, None] = None,
            blur_radius: Union[int, None] = None,
            blur_offset: Union[Tuple[int, int], None] = None
        ) -> None:
        '''
        Initializes the CustomEditListDisplay with the given parameters to create a scrollable table-like display of flows.

        Args:
            parent (QWidget): The parent widget for this display.
            main_app_instance (QObject): The main application instance providing access to shared resources and flows.
            style_sheet (str): The CSS style sheet for styling the CustomEditListDisplay widget.
            geometry (Tuple[int, int, int, int]): The geometry (x, y, width, height) for positioning and sizing the widget.
            field_font (Union[QFont, None], optional): The font used for field labels (default is None).
            grid_font (Union[QFont, None], optional): The font used for grid cell contents (default is None).
            blur_radius (Union[int, None], optional): The radius for the drop shadow effect (default is None).
            blur_offset (Union[Tuple[int, int], None], optional): The (x, y) offset for the drop shadow effect (default is None).
        '''
        super().__init__(parent)

        # Create a QVBoxLayout to contain the scroll area
        main_layout = QVBoxLayout(self)

        # Create and configure the scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its contents
        main_layout.addWidget(scroll_area)

        # Customize the QScrollArea's scroll bar style
        scroll_area.setStyleSheet(scroll_bar_style_sheet)

        # Create a container widget to hold the grid layout
        container_widget = QWidget()
        scroll_area.setWidget(container_widget)

        # Create the grid layout
        grid_layout = QGridLayout(container_widget)

        # Set the spacing between widgets
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(10, 10, 10, 10)  # Set left, top, right, bottom margins

        # Create the header labels for each column
        state_field_label = QLabel('State')
        size_field_label = QLabel('Size')
        category_field_label = QLabel('Category')
        time_executed_field_label = QLabel('Time')
        recurrent_field_label = QLabel('Recurrs')
        actions_field_label = QLabel('Actions')

        if field_font:
            state_field_label.setFont(field_font)
            size_field_label.setFont(field_font)
            category_field_label.setFont(field_font)
            time_executed_field_label.setFont(field_font)
            recurrent_field_label.setFont(field_font)
            actions_field_label.setFont(field_font)

        # Add the field labels to the grid layout
        grid_layout.addWidget(state_field_label, 0, 0, alignment=Qt.AlignCenter)
        grid_layout.addWidget(size_field_label, 0, 1, alignment=Qt.AlignCenter)
        grid_layout.addWidget(category_field_label, 0, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(time_executed_field_label, 0, 3, alignment=Qt.AlignCenter)
        grid_layout.addWidget(recurrent_field_label, 0, 4, alignment=Qt.AlignCenter)
        grid_layout.addWidget(actions_field_label, 0, 5, 1, 2, alignment=Qt.AlignCenter)

        # Sort the flows so the ones needing execution soonest are first
        flows = sorted(
            main_app_instance.manager.ledger.get_projected_flows(),
            key=lambda f: (f.time_executed + timedelta(days=f.recurrent) - datetime.now()).total_seconds()
        )

        # Populate the grid with flow data
        for i, flow in enumerate(flows, start=1):
        # for i, flow in enumerate(main_app_instance.manager.ledger.get_projected_flows(), start=1):
            padding_style_sheet = 'padding: 5px 0px,5px 0px;'

            # Create labels for each field in the flow and apply styles
            size_label = QLabel(str(flow.size))
            size_label.setStyleSheet(padding_style_sheet)
            category_label = QLabel(str(flow.category))
            category_label.setStyleSheet(padding_style_sheet)
            time_executed_label = QLabel(str(flow.time_executed.date()))
            time_executed_label.setStyleSheet(padding_style_sheet)
            recurrent_label = QLabel(str(flow.recurrent))
            recurrent_label.setStyleSheet(padding_style_sheet)

            if grid_font:
                size_label.setFont(grid_font)
                category_label.setFont(grid_font)
                time_executed_label.setFont(grid_font)
                recurrent_label.setFont(grid_font)
            
            # Determine the status style sheet based on flow size
            if flow.size > 0:
                status_style_sheet = 'background-color: green; border-radius: 5px; margin: 5px 0px 5px 0px;'
            else:
                status_style_sheet = 'background-color: red; border-radius: 5px; margin: 5px 0px 5px 0px;'
            
            # Create a status label (CustomLabel) that displays hover text with comments
            status_label = CustomLabel(
                text='',
                parent=None,
                geometry=(0, 0, 50, 10),
                style_sheet=status_style_sheet,
                hover_text=flow.comments,
                hover_style_sheet='color: black;'
            )
            status_label.setFixedHeight(50)
            status_label.setFixedWidth(10)

            # Add the status label and other flow details to the grid layout
            grid_layout.addWidget(status_label, 2*i, 0, Qt.AlignCenter)
            grid_layout.addWidget(size_label, 2*i, 1, alignment=Qt.AlignCenter)
            grid_layout.addWidget(category_label, 2*i, 2, alignment=Qt.AlignCenter)
            grid_layout.addWidget(time_executed_label, 2*i, 3, alignment=Qt.AlignCenter)
            grid_layout.addWidget(recurrent_label, 2*i, 4, alignment=Qt.AlignCenter)

            # Create and add the execute button for the flow
            execute_button = ExecuteFlowButton(
                main_app_instance=main_app_instance,
                flow_id=flow.flow_id,
                sign=1 if flow.size > 0 else -1,
                parent=None,
                size=(80, 50),
                pos=(0, 0),
                style_sheet=green_button_style_sheet,
                font=grid_font,
                blur_radius=1,
                blur_offset=(1, 1),
            )
            grid_layout.addWidget(execute_button, 2*i, 5, alignment=Qt.AlignCenter)
            
            # Create and add the remove button for the flow
            remove_button = DeleteFlowButton(
                main_app_instance=main_app_instance,
                flow_id=flow.flow_id,
                parent=None,
                size=(80, 50),
                pos=(0, 0),
                style_sheet=red_button_style_sheet,
                font=grid_font,
                blur_radius=1,
                blur_offset=(1, 1),
            )
            grid_layout.addWidget(remove_button, 2*i, 6, alignment=Qt.AlignCenter)

            # Add shadow separators between rows, except the last one
            if i < len(main_app_instance.manager.ledger.get_projected_flows()):
                shadow_label = QLabel('')
                shadow_label.setFixedHeight(1)
                shadow_label.setGraphicsEffect(CustomDropShadow(4, (0, 4)))

                # Span the shadow separator across all columns
                grid_layout.addWidget(shadow_label, 2*i + 1, 0, 1, 7)

        # Set the layout for the container widget
        container_widget.setLayout(grid_layout)

        self.setStyleSheet(style_sheet)
        self.setGeometry(*geometry)

        if blur_radius and blur_offset:
            self.setGraphicsEffect(CustomDropShadow(blur_radius, blur_offset))
