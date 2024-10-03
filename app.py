from src.gui.authentication import AuthenticationApp

from PyQt5.QtWidgets import QApplication

import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Initialize the authentication screen (will display the app after loging in)
    auth = AuthenticationApp()
    auth.show()

    sys.exit(app.exec_())  # Start the event loop
