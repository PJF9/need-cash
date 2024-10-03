# NeedCash - Cashflow Management

**NeedCash** is a Python-based desktop application designed to help users manage their cash flow. It allows you to record and track executed transactions and future projections, ensuring clear cashflow visibility. The application uses a graphical user interface (GUI) built with PyQt5, and supports saving/loading the ledger for future use.

## Features

- **Track Cashflows:** Add executed transactions and future projections.
- **Ledger Management:** Separate executed flows from projected ones.
- **Flow Recurrence:** Support for recurrent flows (e.g., recurring expenses).
- **Balance Calculations:** Get current balance, future balance projections, and past monthly balances.
- **GUI Interface:** User-friendly PyQt5 interface to display, add, and manage cashflows.
- **Save/Load Ledger:** Easily save and load your ledger to/from disk using a simple pickle serialization.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)

---

## Project Structure

NEEDCASH/
├── env/                  # Virtual environment (optional)
├── src/                     
│   ├── flow.py           # Flow class (cashflow data model)
│   ├── ledger.py         # Ledger class (ledger data model)
│   ├── gui/                 
│   │   ├── assets/...    # Logo and icons for the widgets
│   │   ├── screens/...   # The screens of the application
│   │   ├── utils/...     # The custom fonts and style sheets for the widgets
│   │   ├── widgets/...   # The custom widgets used in the application
│   │   ├── main_app.py
│   │   ├── authenticaton.py
│   │   ├── app_manager.py   
│   └── utils/               
│       ├── balance.py
│       └── save.py
├── requirements.txt
├── .gitignore
├── README.md
└── app.py    # The need-cash application

## Installation

### Prerequisites

Make sure you have the following installed:
- **Python 3.8+**
- **pip** (Python package manager)

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/needcash.git
   cd needcash
   ```

2. (Optional) Create a virtual environment to isolate dependencies:
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows use: env\Scripts\activate
    ```

3. Install dependencies from requirements.txt:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python app.py
    ```

## Usage

### Using the GUI

* **Authenticate**: Use the testing ledger (username and password 'test') to explore the application. Otherwise, create a new account, which you can log into later.
* **Adding a Flow**: You can add both executed and projected flows using the "Add Flow" option in the application.
* **Viewing the Ledger**: The ledger shows both executed and projected flows using the "See Flows" option in the application.
* **Calculating Future Balance**: You can project the future balance up to a given date using the application's right arrow button.
* **Saving and Loading**: After adding, executing, or deleting a flow, the ledger is saved automatically.

---

# Contributions

Feel free to fork this repository and create pull requests for improvements or bug fixes. We welcome contributions that make **NeedCash** even better!
