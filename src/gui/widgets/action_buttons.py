from src.utils.save import save_ledger
from src.gui.widgets.buttons import CustomPushButton
from src.gui.widgets.dial_window import FlowSizeInputDialog, ConfirmDeleteDialog

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QObject

from datetime import datetime
from typing import Union, Tuple


class ExecuteFlowButton(CustomPushButton):
    '''
    The `ExecuteFlowButton` class represents a custom push button that triggers the execution of a flow when clicked.
    It inherits from `CustomPushButton` and provides additional functionality for handling flow execution,
    including prompting the user to input the real size of the flow and processing this input accordingly.
    '''
    def __init__(self,
            main_app_instance: QObject,
            flow_id: int,
            sign: int,
            parent: QObject,
            size: Tuple[int, int],
            pos: Tuple[int, int],
            style_sheet: str,
            font: Union[QFont, None]=None,
            blur_radius: Union[int, None]=None,
            blur_offset: Union[Tuple[int, int], None]=None
        ) -> None:
        '''
        Initializes the ExecuteFlowButton with the given parameters, setting up the button to handle the execution
        of a specific flow.

        Args:
            main_app_instance (QObject): The main application instance providing access to shared resources and functionality.
            flow_id (int): The unique identifier of the flow that this button will execute.
            sign (int): The multiplier (either -1 or 1) used to adjust the real size of the flow based on the sign.
            parent (QObject): The parent widget that contains this button.
            size (Tuple[int, int]): The (width, height) size of the button.
            pos (Tuple[int, int]): The (x, y) position of the button within the parent widget.
            style_sheet (str): The CSS style sheet used to style the button.
            font (Union[QFont, None], optional): The font used for the button text (default is None).
            blur_radius (Union[int, None], optional): The radius for the blur effect applied to the button (default is None).
            blur_offset (Union[Tuple[int, int], None], optional): The (x, y) offset for the blur effect (default is None).
            '''
        self.main_app_instance = main_app_instance
        self.flow_id = flow_id
        self.sign = sign

        super().__init__(
            text='Execute',
            parent=parent,
            size=size,
            pos=pos,
            style_sheet=style_sheet,
            font=font,
            blur_radius=blur_radius,
            blur_offset=blur_offset,
            on_click=self.execute
        )

    def execute(self) -> None:
        '''
        Handles the logic for executing the flow when the button is clicked. It prompts the user to enter
        the real size of the flow using an input dialog, processes the input, and executes the flow accordingly.
        The method performs the following steps:
        
        1. Opens a `FlowSizeInputDialog` to prompt the user to enter the real flow size.
        2. If the input is valid, it converts the input value to a float, applies the sign multiplier, and executes the flow.
        3. Updates the ledger with the executed flow and saves it to the specified path.
        4. Reloads all windows to reflect the changes.
        5. Switches the application screen to the 'edit_pending_flows_screen'.
        
        If the input is invalid (empty string), it recursively calls itself to retry the process.

        Returns:
            None
        '''
        # Create and display the input dialog
        dialog = FlowSizeInputDialog(parent=self.parent())
        result = dialog.exec_()
        
        # Check if the dialog was accepted
        if result == QDialog.Accepted:
            real_size = dialog.get_input()

            if real_size != '':
                # Convert the input to a float, applying the sign multiplier
                real_size_value = float(real_size.replace(',', '.')) * self.sign

                # Execute the flow on the ledger
                self.main_app_instance.manager.ledger.execute_flow(self.flow_id, real_size_value, datetime.now())

                # Save the updated ledger
                save_ledger(self.main_app_instance.manager.ledger, save_path=self.main_app_instance.manager.path)

                # Relaod all windows to add the new flow
                self.main_app_instance.reload_windows()

                # Switch to the next screen
                self.main_app_instance.fade_out_and_switch('see_flows_screen')
            else:
                # Go back to the dial widget if got invalid entry
                self.execute()


class DeleteFlowButton(CustomPushButton):
    '''
    A custom push button that allows the user to delete a flow from the ledger. When clicked, it prompts
    a confirmation dialog asking the user if they want to delete the specified flow.

    This button is initialized with details about the flow it manages and the main application instance 
    to facilitate deletion and data updates.
    '''
    def __init__(self,
            main_app_instance: QObject,
            flow_id: int,
            parent: QObject,
            size: Tuple[int, int],
            pos: Tuple[int, int],
            style_sheet: str,
            font: Union[QFont, None]=None,
            blur_radius: Union[int, None]=None,
            blur_offset: Union[Tuple[int, int], None]=None
        ) -> None:
        '''
        Initializes the DeleteFlowButton instance with the provided parameters.

        Args:
            main_app_instance (QObject): The main application instance providing access to shared resources and functionality.
            flow_id (int): The unique identifier of the flow that this button will execute.
            parent (QObject): The parent widget that contains this button.
            size (Tuple[int, int]): The (width, height) size of the button.
            pos (Tuple[int, int]): The (x, y) position of the button within the parent widget.
            style_sheet (str): The CSS style sheet used to style the button.
            font (Union[QFont, None], optional): The font used for the button text (default is None).
            blur_radius (Union[int, None], optional): The radius for the blur effect applied to the button (default is None).
            blur_offset (Union[Tuple[int, int], None], optional): The (x, y) offset for the blur effect (default is None).
            '''
        self.main_app_instance = main_app_instance
        self.flow_id = flow_id

        super().__init__(
            text='Delete',
            parent=parent,
            size=size,
            pos=pos,
            style_sheet=style_sheet,
            font=font,
            blur_radius=blur_radius,
            blur_offset=blur_offset,
            on_click=self.delete
        )

    def delete(self) -> None:
        '''
        Triggered when the delete button is clicked. It opens a confirmation dialog asking the user to confirm
        the deletion of the flow. If confirmed, it proceeds to delete the flow from the ledger, save the updated 
        ledger, and reload all windows to reflect the changes.

        Returns:
            None.
        '''
        # Create the delete confirmation dialog
        dialog = ConfirmDeleteDialog(parent=self)
        result = dialog.exec_()
        
        # Check if the user confirmed the deletion
        if result == QDialog.Accepted:
            # Delete the projected flow from the ledger
            self.main_app_instance.manager.ledger.remove_projected_flow(self.flow_id)
            
            # Save the updated ledger
            save_ledger(self.main_app_instance.manager.ledger, save_path=self.main_app_instance.manager.path)
            
            # Reload all windows to reflect the change
            self.main_app_instance.reload_windows()
            self.main_app_instance.fade_out_and_switch('edit_pending_flows_screen')
