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

NEEDCASH/<br>
├── env/                  # Virtual environment (optional)<br>
├── src/<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── flow.py           # Flow class (cashflow data model)<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── ledger.py         # Ledger class (ledger data model)<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── gui/<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── assets/...    # Logo and icons for the widgets<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── screens/...   # The screens of the application<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── utils/...     # The custom fonts and style sheets for the widgets<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── widgets/...   # The custom widgets used in the application<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── main_app.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── authenticaton.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── app_manager.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── utils/<br>
│       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── balance.py<br>
│       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── save.py<br>
├── requirements.txt<br>
├── .gitignore<br>
├── README.md<br>
└── app.py    # The need-cash application<br>

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
