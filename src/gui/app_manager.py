from src.flow import Flow
from src.ledger import Ledger
from src.utils.save import load_ledger, save_ledger
from src.utils.balance import get_balance, get_balance_state

from pathlib import Path
from datetime import datetime
from typing import List


class AppManager:
    '''
    AppManager handles the core application logic and manages interactions with the ledger.
    '''
    def __init__(self, ledger_path: str, _account_name: str=''):
        '''
        Initialize the AppManager instance.

        Args:
            ledger_path (str): The file path where the ledger is stored or should be created.
            _account_name (str): The account name that will be given to the ledger, if
                the ledger path doesn't exist.
        '''
        self.path = ledger_path
        self.ledger = self.__ledger_from_path(_account_name)
        
        # The temporary flow (id 0) that will be used on the add flow screens and finally will be added to the ledger
        self._flow: Flow = Flow(size=0, category='', time_executed=datetime(2024, 1, 9))

        # After the temporary flow has been initialized, move the flow_id to prvent id collisions        
        Flow._id_counter = self.ledger.last_id
        
    def __ledger_from_path(self, account_name: str) -> Ledger:
        '''
        Load the ledger from the given path or create a new one if it doesn't exist.

        Args:
            account_name (str): The account name that will be given to the ledger, if
                the ledger path doesn't exist.
        
        Returns:
            Ledger: An instance of the Ledger class representing the account ledger.
        '''
        if not Path(self.path).is_file():
            # Create parent directories if they don't exist
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)

            # Initialize an empty ledger
            ledger = Ledger(account_name=account_name)

            # Save the new empty ledger to the given path
            save_ledger(ledger, save_path=self.path)
        else:
            # Load the account ledger from the given path
            ledger = load_ledger(self.path)

        return ledger
    
    def get_account_name(self) -> str:
        '''
        Retrieve the account name from the ledger instance.

        Returns:
            str: The account name.
        '''
        return self.ledger.account_name

    def get_n_flows(self) -> int:
        '''
        Get the total number of flows in the ledger, including both executed and projected flows.

        Returns:
            int: The total count of executed and projected flows.
        '''
        return len(self.ledger.get_executed_flows()) + len(self.ledger.get_projected_flows())
    
    def get_n_projections(self) -> int:
        '''
        Get the number of projected flows in the ledger.

        Returns:
            int: The count of projected flows.
        '''
        return len(self.ledger.get_projected_flows())

    def get_n_balance(self) -> float:
        '''
        Retrieve the current balance from the ledger.

        Returns:
            float: The current balance as an integer.
        '''
        return get_balance(self.ledger)
    
    def get_state_balance(self) -> int:
        '''
        Determine the balance state of the account based on the account ledger.

        Returns:
            An integer representing the state of the balance:
                - 1 if the balance is increasing.
                - -1 if the balance is decreasing.
                - 0 if the balance is not changing.
        '''
        return get_balance_state(self.ledger)
    
    def get_to_be_executed_flows(self) -> List[Flow]:
        '''
        Determine which flows need to be executed based on their next execution date.

        Returns:
            List[Flow]: A list of flows scheduled to be executed today.
        '''
        return self.ledger.flows_to_be_executed()
