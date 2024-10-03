from src.ledger import Ledger

from datetime import datetime, timedelta
from calendar import monthrange
from typing import Dict


def get_balance_state(ledger: Ledger) -> int:
    '''
    Determine the balance state of the account based on the projected flows.

    The function evaluates whether the projected flows in the ledger indicate an
    increase, decrease, or no change in the account balance. 

    - If the sum of projected flows is positive, it indicates an expected increase, and the method returns 1.
    - If the sum is negative, it indicates an expected decrease, and the method returns -1.
    - If the sum is zero, it indicates no change, and the method returns 0.

    Args:
        ledger (Ledger): An instance of the Ledger class containing account flow data.
    
    Returns:
        int: An integer representing the state of the balance
    '''
    sum_of_projected = sum(flow.size for flow in ledger._flows['projected'])

    if sum_of_projected > 0:
        return 1
    elif sum_of_projected < 0:
        return -1
    return 0


def get_balance(ledger: Ledger, _timestamp: datetime=datetime.now()) -> float:
    '''
    Calculate the total balance from the executed flows.

    Args:
        ledger (Ledger): An instance of the Ledger class containing account flow data.
        _timestamp (datetime): The time that the balance will be calculated based on.
        
    Returns:
        float: The balance of the account derived from the different flows that the ledger has captured.
    '''
    return sum(flow.size for flow in ledger._flows['executed'] if flow.time_executed.date() <= _timestamp.date())


def get_future_balance(ledger: Ledger, timestamp: datetime) -> float:
    '''
    Calculates the projected balance for the ledger at a future point in time.

    This method starts with the current balance and adds all projected flows 
    that are scheduled to occur up until the given timestamp. Recurrent flows 
    are applied multiple times based on how many periods have passed by the given time.

    Args:
        ledger (Ledger): An instance of the Ledger class containing account flow data.
        timestamp (datetime): The future point in time to calculate the balance for.

    Returns:
        float: The projected balance at the given future timestamp.
    '''
    # Get current balance
    balance = get_balance(ledger)

    for proj_flow in ledger._flows['projected']:
        # Ensure flow is projected for a date before or on the given timestamp
        if proj_flow.time_executed <= timestamp:
            # For non-recurrent flows (recurrent == 0), only add once if before the timestamp
            if proj_flow.recurrent == 0:
                balance += proj_flow.size
            else:
                # Get days from the date the flow was placed until the given timestamp
                days = (timestamp - proj_flow.time_executed).days
                # Calculate how many times this flow will be executed until the given timestamp
                times_executed = days // proj_flow.recurrent
                # Update the current balance with the projected flow amount
                balance += (proj_flow.size * times_executed)

    return balance


def get_future_monthly_balances(ledger: Ledger, end_timestamp: datetime) -> Dict[str, float]:
    '''
    Calculates the total balance at the end of each month from the current date (datetime.now())
    until the given end_timestamp.

    The balance is calculated by using the get_future_balance() method for each month-end date 
    up to the given timestamp.

    Args:
        ledger (Ledger): An instance of the Ledger class containing account flow data.
        end_timestamp (datetime): The future point in time up to which monthly balances are calculated.

    Returns:
        Dict[str, float]: A dictionary where the keys are strings representing each month (e.g. "2024-09")
        and the values are the total balance at the end of each month.
    '''
    # Dictionary to store the balances at the end of each month
    monthly_balances = {}

    current_date = datetime.now()

    while current_date <= end_timestamp:
        # Calculate the last day of the current month
        _, last_day = monthrange(current_date.year, current_date.month)
        # Get the timestamp of the last day of each month
        end_of_month = current_date.replace(day=last_day, hour=23, minute=59, second=59)
        
        # Check if the end of the month exceeds the end timestamp
        if end_of_month > end_timestamp:
            end_of_month = end_timestamp

        # Use get_future_balance() to calculate the balance at the end of the current month
        balance = get_future_balance(ledger, end_of_month)

        # Store the balance for the current month (as "YYYY-MM")
        month_key = f"{current_date.year}-{current_date.month:02d}"
        balance = f'{balance:.2f}'
        monthly_balances[month_key] = float(balance)

        # Move to the first day of the next month using a simple trick
        next_month = current_date.replace(day=28) + timedelta(days=4)  # this will always take you to the next month for every 'current_date'
        # Get the first timestamp of the new month
        current_date = next_month.replace(day=1)

    return monthly_balances


def get_past_monthly_balances(ledger: Ledger, end_timestamp: datetime) -> Dict[str, float]:
    '''
    Calculates the total balance for each month based only on executed flows
    from the current date going backwards in time until the given end_timestamp.

    The function returns a dictionary where the key is a string representing
    the year and month (e.g., '2024-09'), and the value is the total balance
    for that month.

    Args:
        ledger (Ledger): The ledger containing executed flows.
        end_timestamp (datetime): The earliest date to consider when calculating monthly balances.
    
    Returns:
        Dict[str, float]: A dictionary mapping each month to its corresponding total balance.
    '''
    monthly_balances = {}

    current_date = datetime.now()
    balance = get_balance(ledger=ledger)

    # Loop backward through the months until reaching end_timestamp
    while current_date >= end_timestamp:
        # Get the last day of the current month
        _, last_day = monthrange(current_date.year, current_date.month)
        
        # Define the start and end of the current month
        end_of_month = current_date.replace(day=last_day, hour=23, minute=59, second=59)
        start_of_month = current_date.replace(day=1, hour=0, minute=0, second=0)
        
        # Ensure that the start date does not go beyond the end_timestamp
        if start_of_month < end_timestamp:
            start_of_month = end_timestamp

        balance = get_balance(ledger=ledger, _timestamp=end_of_month)
        # start_balance = get_balance(ledger=ledger, _timestamp=start_of_month)

        # balance = balance - start_balance

        # Calculate the balance for this month from executed flows
        # balance = 0
        # for exec_flow in ledger._flows['executed']:
        #     if exec_flow.time_executed >= start_of_month and exec_flow.time_executed <= end_of_month:
        #         balance += exec_flow.size

        # Format the key as YYYY-MM
        month_key = f"{current_date.year}-{current_date.month:02d}"
        monthly_balances[month_key] = balance

        # Move to the previous month
        current_date = current_date.replace(day=1) - timedelta(days=1)

    # Farward pass to update the balance for each month
    # balances = list(monthly_balances.values())
    # for i in range(len(balances) - 1):
    #     balances[i] += balances[i+1]

    # for i, key in enumerate(monthly_balances.keys()):
    #     monthly_balances[key] = balances[i]

    return monthly_balances
