from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Flow:
    '''
    This class represents a financial flow (either inflow or outflow) for cash flow management.
    
    Attributes:
        flow_id (int): A unique identifier for each flow instance. It is automatically generated and incremented
            for every new instance.
        size (float): The amount of the flow. This represents the size of the cash movement, either positive (inflow)
            or negative (outflow).
        category (str): A category identifier to classify the type of flow (e.g., income, expense, etc.).
        time_executed (datetime): The time at which the flow is placed on the ledger.
            If a flow is not a projection it means that this time is the time that the flow has been executed.
            If a flow is a projection then this time indicates either the first time this flow is going to be executed,
            or the last time this flow has been executed.
        recurrent (int): Defines how frequently the flow recurs. The default value is 0, meaning the flow is
            non-recurrent. If greater than 0, it specifies the number of days after which the flow recurs.
        comments (str): Comments about the flow. Extra notes from the user. Default is empty string.

    Class Attributes:
        _id_counter (int): A class-level static variable used to automatically assign unique IDs to each instance of
            `Flow`. This counter increments for every new instance and is not included in the instance's
            representation (`__repr__`).
    '''
    flow_id: int = field(init=False) # the id will be set automatically, not passed to __init__
    size: float
    category: str
    time_executed: datetime
    recurrent: int = 0
    comments: str = ''

    # Class variable to track the last assigned ID
    _id_counter: int = field(default=-1, init=False, repr=False)
    # default is -1 because the flow with id=0 is going to be the placeholder for the temporary flow in the app

    def __post_init__(self):
        '''
        Increment the class-level counter and assign a unique ID to each instance.
        This ensures that each `Flow` object has a unique `flow_id`.
        '''
        Flow._id_counter += 1
        self.flow_id = Flow._id_counter

    def clear(self) -> None:
        '''
        Reset the state of a flow
        '''
        self.size = 0
        self.category = ''
        self.time_executed = datetime(2024, 1, 1, 0, 0, 0)
        self.recurrent = 0
        self.comments = ''

    def copy(self) -> 'Flow':
        '''
        Deepcopy a given flow

        Returns:
            Flow: The flow that contains the same data as self, with different `flow_id`.
        '''
        return Flow(
            size=self.size,
            category=self.category,
            time_executed=self.time_executed,
            recurrent=self.recurrent,
            comments=self.comments
        )
