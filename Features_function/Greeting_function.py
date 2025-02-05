import sys
import os
import random
#Add the root directory to the pyhton  path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Data.Wish_data.Greeting_dialog_data import Greeting_responses as Greetings_data

def Greetings():
    """
    Function to greet the user with a random message from the Greetings data.
    """
    greeting = random.choice(Greetings_data)
    message = f"{greeting}"
    return message