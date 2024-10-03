from src.gui.widgets.label import CustomLabel
from src.gui.widgets.buttons import CustomPushButton
from src.gui.widgets.input_box import CustomInputBox
from src.gui.widgets.logo import LogoLabel
from src.gui.main_app import NeedCashApp
from src.gui.app_manager import AppManager
from src.gui.utils.style_sheets import (
    action_prompt_style_sheet,
    buttons_style_sheet,
    magnitude_input_box_style_sheet
)
from src.gui.utils.fonts import (
    action_prompt_font,
    button_font,
    magnitude_font
)

from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon

import hashlib
import json


class AuthenticationApp(QWidget):
    '''
    AuthenticationScreen class represents the interface for loging into the
    application.
    '''
    def __init__(self) -> None:
        '''
        Initializes the AuthenticationScreen.

        Args:
            parent (QObject): The parent widget that provides context and functionality 
                for screen transitions.
        '''
        super().__init__()

        # Set window properties
        self.setWindowTitle('NeedCash')
        self.setGeometry(100, 100, 1100, 800)
        self.setStyleSheet('background-color: #ffffff;')
        self.setFixedSize(1100, 800)

        # Set the window icon
        self.setWindowIcon(QIcon('src/gui/assets/needcash_icon.png'))

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

        # Setting the action prompt label
        CustomLabel(
            text='Welcome to NeedCash!\nPlease log in or register to continue.',
            parent=self.screen_frame,
            geometry=(10, 120, 1050, 100),
            style_sheet=action_prompt_style_sheet,
            font=action_prompt_font
        )

        # Swtting the account name label and input box
        CustomLabel(
            text='Account Name',
            parent=self.screen_frame,
            geometry=(330, 250, 250, 30),
            style_sheet=magnitude_input_box_style_sheet,
            font=magnitude_font
        )
        self.name_box = CustomInputBox(
            parent=self.screen_frame,
            style_sheet=magnitude_input_box_style_sheet,
            geometry=(330, 290, 400, 80),
            font=magnitude_font,
            blur_radius=3,
            blur_offset=(3, 3)
        )

        # Setting the passward label and input box
        CustomLabel(
            text='Account Passward',
            parent=self.screen_frame,
            geometry=(330, 410, 300, 30),
            style_sheet=magnitude_input_box_style_sheet,
            font=magnitude_font

        )
        self.passwd_box = CustomInputBox(
            parent=self.screen_frame,
            style_sheet=magnitude_input_box_style_sheet,
            geometry=(330, 460, 400, 80),
            font=magnitude_font,
            blur_radius=3,
            blur_offset=(3, 3)
        )
        self.passwd_box.setEchoMode(QLineEdit.Password)

        # Setting the login or register button
        CustomPushButton(
            text='Login/Register',
            parent=self.screen_frame,
            size=(250, 80),
            pos=(400, 610),
            style_sheet=buttons_style_sheet,
            font=button_font,
            blur_radius=1,
            blur_offset=(1, 1),
            on_click=self.next_button_pressed
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
    
    @staticmethod
    def __hash_password(plain_password: str) -> str:
        '''
        Hashes a plain password using a deterministic approach with a fixed salt.

        This method utilizes the PBKDF2 (Password-Based Key Derivation Function 2) algorithm
        with HMAC and SHA-256 to generate a secure hash of the provided password. The use of a 
        fixed salt ensures that the hashing is deterministic, meaning that the same password 
        will always yield the same hash. This method is primarily used for account password 
        storage.

        Args:
            plain_password (str): The plain text password to be hashed.

        Returns:
            str: The resulting hashed password in hexadecimal format.
        '''
        # Use a fixed salt to make the function deterministic, or omit it entirely.
        fixed_salt = b'NeedCash App'  # This makes the hash deterministic

        # Combine the salt with the password and hash it using SHA-256
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',                        # Hashing algorithm
            plain_password.encode('utf-8'),  # Convert the password to bytes
            fixed_salt,                      # Use the fixed salt
            100000                           # Number of iterations (increase for more security)
        )

        # Return the salt and the hashed password as a combined string (for storage)
        return password_hash.hex()
    
    def __open_main_app(self, name: str) -> None:
        '''
        Helper function to initialize and open the main application.

        Returns:
            None.
        '''
        app_manager = AppManager(f'./ledgers/ledger_{name}.pkl', _account_name=name)
        window = NeedCashApp(manager=app_manager)
        self.close()
        window.show()

    def next_button_pressed(self) -> None:
        '''
        Handles the event when the 'Next' button is pressed.

        Returns:
            None.
        '''
        name, passwd = self.name_box.text(), self.__hash_password(self.passwd_box.text())
        
        if not name or not passwd:
            return self.reload_widgets()  # Reload if fields are empty

        with open('./accounts.json', 'r+') as f:
            accounts = json.load(f)

            if name in accounts:
                if passwd == accounts[name]:
                    self.__open_main_app(name)  # Open the app if credentials are correct
                else:
                    self.reload_widgets()  # Reload if password is incorrect
            else:
                accounts[name] = passwd
                f.seek(0)  # Move to the beginning of the file to overwrite
                json.dump(accounts, f)
                f.truncate()  # Remove any leftover data
                self.__open_main_app(name)  # Create a new account and open the app

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
