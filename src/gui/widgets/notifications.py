from src.flow import Flow
from src.gui.widgets.label import CustomLabel
from src.gui.utils.fonts import (
    notifications_font,
    notifications_hover_font
)

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, Qt

from typing import List


class CustomNotificationsDisplay(QWidget):
    '''
    CustomNotificationsDisplay is a QWidget subclass that displays notifications 
    for pending flows in a user interface. It shows the number of pending flows and 
    provides hover text with details for each flow.
    '''
    def __init__(self,
            parent: QObject,
            flows: List[Flow],
        ) -> None:
        '''
        Initializes the CustomNotificationsDisplay with a parent widget and a list of pending flows.

        Args:
            parent (QObject): The parent widget for this notifications display.
            flows (List[Flow]): A list of Flow objects that are pending for execution.
        
        '''
        super().__init__(parent)

        self.flows = flows

        # Setting the text label
        CustomLabel(
            text=f'{len(flows)} Flow(s) are Pending for Execution',
            parent=self,
            geometry=(600, 20, 440, 55),
            style_sheet='background-color: white; padding: 15px; border-radius: 10px',
            font=notifications_font,
            blur_radius=1,
            blur_offset=(1, 1),
            hover_text=self.__setup_hover_text(),
            hover_style_sheet='background-color: white;',
            hover_font=notifications_hover_font
        ).setAlignment(Qt.AlignRight)

        # Setting the notifications icon
        label = QLabel(self)
        label.setPixmap(QPixmap('./src/gui/assets/notifications_icon_2.png' if len(flows) == 0 else './src/gui/assets/notifications_icon.png'))
        label.setFixedSize(35, 35)
        label.setScaledContents(True)
        label.move(613, 31)

    def __setup_hover_text(self) -> str:
        '''
        Prepares the hover text for the notification display.

        The hover text lists the details of each pending flow, including its size 
        and category. If there are no flows, it returns None.

        Returns:
            str: A formatted string containing details of the pending flows or None 
                  if there are no flows.
        '''
        if len(self.flows) != 0:
            hover_text = ''
            for i in range(len(self.flows)):
                hover_text += f'> Size {self.flows[i].size:.2f} | Category: {self.flows[i].category}'
                if i != len(self.flows) - 1:
                    hover_text += '\n\n'

            return hover_text
        return None
