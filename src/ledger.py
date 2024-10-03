from src.flow import Flow

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Union, List, Tuple


@dataclass
class Ledger:
    '''
    Ledger class manages cash flow entries, distinguishing between projected flows and executed flows.
    Projected flows are modifiable, while executed flows are immutable once they are marked as executed.
    
    Attributes:
        account_name (str): The name of the account the ledger is responsible for.
        _flows (Dict[str, Union[List[Flow], Tuple[Flow, ...]]]): 
            A dictionary that stores two types of flows:
            - 'projected' (List[Flow]): A list of projected flows, which are modifiable until executed.
            - 'executed' (Tuple[Flow, ...]): An immutable tuple of executed flows.
        last_id (int): The id of the last added flow. Will be usefull for keeping the flow with id=0
            as the temporary flow of the app.
    '''
    account_name: str
    _flows: Dict[str, Union[List[Flow], Tuple[Flow, ...]]] = field(init=False)
    last_id: int = 0

    def __post_init__(self):
        '''
        Initializes the ledger by creating an empty list for projected flows and an empty tuple for executed
        flows. This structure ensures that projected flows can be modified and executed flows remain immutable.
        '''
        self._flows = {
            'executed': (),
            'projected': []
        }

    def get_executed_flows(self) -> Tuple[Flow]:
        '''
        Return the executed flows.

        Returns:
            Tuple[Flow]: The tuple containing all the executed flows.
        '''
        return self._flows['executed']
    
    def get_projected_flows(self) -> List[Flow]:
        '''
        Return the projected flows.

        Returns:
            List[Flow]: The list containing all the projected flows.
        '''
        return self._flows['projected']
    
    def add_flow(self, flow: Flow, is_proj: bool=False) -> None:
        '''
        Adds a new flow to the ledger if it does not already exist.
        
        If the flow has not yet been executed (`time_executed` is `None`), it is added to the 'projected' list.
        If the flow has already been executed (`time_executed` is not `None`), it is added to the 'executed'
        tuple directly.
        
        Args:
            flow (Flow): The flow instance to be added
            is_proj (bool): Whether the flow is a projection (has not yet been executed). Default is False.
        '''
         # Check if the flow already exists in the projected flows
        for existing_flow in self._flows['projected']:
            if existing_flow.flow_id == flow.flow_id:
                print(f"Flow with ID {flow.flow_id} already exists in projected flows.")
                return  # Early exit to prevent duplicate
        
        # Check if the flow already exists in the executed flows
        for existing_flow in self._flows['executed']:
            if existing_flow.flow_id == flow.flow_id:
                print(f"Flow with ID {flow.flow_id} already exists in executed flows.")
                return  # Early exit to prevent duplicate

        if is_proj:
            self._flows['projected'].append(flow)
        else:
            self._flows['executed'] += (flow,)

        self.last_id = flow.flow_id

    def execute_flow(self, flow_id: int, real_size: float, time_executed: datetime) -> bool:
        '''
        Marks a projected flow as executed by moving it to the 'executed' section.
        
        The flow is found in the 'projected' list using its `flow_id`. 
        Once found, its size is updated to the `real_size`, and `time_executed` is set to the provided `time_executed`.
        It is then moved to the 'executed' tuple, and removed from the 'projected' list.
        
        Args:
            flow_id (int): The unique ID of the flow to be executed.
            real_size (float): The actual size of the flow at execution time.
            time_executed (datetime): The timestamp when the flow is to be placed on the ledger.
            
        Returns:
            bool: `True` if the flow is successfully executed and moved, `False` if the flow was not found.
        '''
        for flow in self._flows['projected']:
            if flow.flow_id == flow_id:
                # Create a new flow so I can add a projected recurrent flow int the executed set 
                new_flow = Flow(
                    size=real_size,
                    category=flow.category,
                    time_executed=time_executed,
                    recurrent=flow.recurrent,
                    comments=flow.comments
                )

                # Add the flow into the executed set
                self._flows['executed'] += (new_flow,)

                if flow.recurrent == 0:
                    # If a flow is not recurrent remove it from the projection list
                    self._flows['projected'].remove(flow)
                else:
                    # If a flow is recurrent add as execution time the last time the flow has been executed
                    flow.time_executed = time_executed
                return True
            
        return False
    
    def remove_projected_flow(self, flow_id: int) -> bool:
        '''
        Removes a projected flow from the ledger by its flow ID.

        Args:
            flow_id (int): The ID of the flow to be removed from the 'projected' flows.

        Returns:
            bool: True if the flow was successfully removed, False if no flow with the given ID was found.
        '''
        initial_count = len(self._flows['projected'])

        # Use list comprehension to filter out the flow with the given ID
        self._flows['projected'] = [flow for flow in self._flows['projected'] if flow.flow_id != flow_id]
        
        # If the list length changed, the flow was successfully removed
        return len(self._flows['projected']) < initial_count

    def flows_to_be_executed(self) -> List['Flow']:
        '''
        Determine which flows need to be executed based on their next execution date.

        Returns:
            List[Flow]: A list of flows scheduled to be executed today.
        '''
        today = datetime.now().date()
        return [
            pending_flow for pending_flow in self._flows['projected']
            if (pending_flow.time_executed + timedelta(pending_flow.recurrent)).date() == today
        ]
