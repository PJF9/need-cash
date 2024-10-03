from src.gui.widgets.shadow import CustomDropShadow

from PyQt5.QtWidgets import QWidget, QVBoxLayout

from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from datetime import datetime
from typing import Union, List, Tuple


class CustomGraphWidget(QWidget):
    '''
    A custom QWidget that displays a graph using Matplotlib integrated within a PyQt5 interface.

    This widget allows plotting a line graph with months on the x-axis and corresponding monetary values on the y-axis.
    It also highlights the current month with a vertical line and displays a zero-balance horizontal line.
    '''
    def __init__(self,
            parent: QWidget,
            current_date: datetime,
            months: List[str],
            values: List[float],
            geometry: Tuple[int, int, int, int],
            blur_radius: Union[int, None]=None,
            blur_offset: Union[Tuple[int, int], None]=None,
        ) -> None:
        '''
        Initializes the CustomGraphWidget.

        Args:
            parent (QWidget): The parent widget for this graph widget.
            current_date (datetime): The current date to mark the present month on the graph.
            months (List[str]): A list of month abbreviations representing the x-axis labels.
            values (List[float]): A list of float values representing monetary data for each month.
            geometry (Tuple[int, int, int, int]): The geometry (x, y, width, height) to set the widget's size and position.
            blur_radius (Union[int, None], optional): The radius of the blur effect. Defaults to None (no blur).
            blur_offset (Union[Tuple[int, int], None], optional): The offset of the blur effect (x, y). Defaults to None (no blur).
        '''
        super().__init__(parent)

        self.months = months
        self.values = values
        self.current_date = current_date

        # Creating the Canvas widget for plotting
        self.canvas = FigureCanvas(Figure(figsize=(8, 5)))

        # Creating the layout that will hold the Canvase
        layout = QVBoxLayout()

        # Adding the Canvas to the layout
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # Render the initial plot
        self.plot()

        self.setGeometry(*geometry)

        if blur_radius and blur_offset:
            self.setGraphicsEffect(CustomDropShadow(blur_radius, blur_offset))

    def plot(self) -> None:
        '''
        Renders the graph with the provided months and values.

        This method sets up the graph with a grid, hides the top and right spines, plots a zero-balance line at y=0,
        marks the current month with a vertical line, and plots the monetary values for each month.

        Returns:
            None.        
        '''
        # Setting up the grid and axes
        ax = self.canvas.figure.add_subplot(111)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

        # Hide the top and right spines for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Plotting the y=0 line to represent zero balance
        ax.plot(self.months, [0] * len(self.months), linestyle='--', color='red', linewidth=1)

        # Highlight the current month if it matches the current year
        if datetime.now().year == self.current_date.year:
            ax.axvline(x=datetime.now().strftime('%b'), color='green', linestyle='--', linewidth=1)

        # Plot the data points for each month
        ax.plot(self.months, self.values, color='purple', marker='o', markersize=5, linewidth=1)

        # Set custom font properties for the x-axis labels
        x_font_properties = FontProperties()
        x_font_properties.set_family('sans-serif')
        x_font_properties.set_size(12)
        x_font_properties.set_weight('bold')

        # Set the tick positions first
        ax.set_xticks(range(len(self.months)))
        
        # Apply font properties to x-tick labels with fixed tick positions
        ax.set_xticklabels(self.months, fontproperties=x_font_properties, rotation=0, ha='center')

        # Render the updated graph on the canvas
        self.canvas.draw()
