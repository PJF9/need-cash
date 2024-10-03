from src.ledger import Ledger

import pickle
from pathlib import Path


def save_ledger(ledger: Ledger, save_path: str) -> bool:
    '''
    Saves the given Ledger instance as a pickle file at the specified location.

    Args:
        ledger (Ledger): The ledger instance to be saved.
        save_path (Union[str, Path]): The path where the ledger should be saved.
    
    Returns:
        bool: Returns `True` if the ledger was successfully saved, otherwise `False`.
    '''
    # Convert path to a pathlib object
    save_path = Path(save_path)

    # If parent path doesn't exists
    if not save_path.parent.exists():
        print(f'Parent path: `{save_path.parent}` doesn\'t exists.')
        return False
    
    # If the file is not a pickle file
    if not save_path.name.endswith('.pkl'):
        print(f'The given file is not a pickle file, doesn\'t end with .pkl')
        return False

    with open(save_path, 'wb') as f:
        pickle.dump(ledger, f)
    
    return True


def load_ledger(load_path: str) -> Ledger:
    '''
    Loads a Ledger instance from the specified pickle file.

        Args:
        load_path (str): The path to the pickle file that contains the saved Ledger.

    Returns:
        Ledger: The loaded Ledger instance. If an error occurs, a new (empty) Ledger instance is returned.
    '''
    try:
        with open(load_path, 'rb') as f:
            ledger = pickle.load(f)
            
        return ledger

    except Exception as e:
        print(f'Error occur: {e}')
        
        return Ledger()
