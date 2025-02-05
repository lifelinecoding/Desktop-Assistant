import sys
import os
import random
import re
#Add the root directory to the pyhton  path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Head.Mouth import Speak, Speak_with_script
from Head.Ear import listen
from Head.Brain import Brain
from Features_function.Wish_function import Make_wish
from Features_function.Greeting_function import Greetings
# from Features_function.Jokes_function import Jokes
from Data.Wish_data.Greeting_dialog_data import Wake_up_commands,Wake_up_responses, Bye_commands, Bye_responses


def clean_command(command):
    """
    Cleans the input command by removing punctuation, extra spaces, and converting it to lowercase.
    """
    return re.sub(r'[^\w\s]', '', command).strip().lower()


def Jarvis():
    try:
        """
        Main function to handle the voice assistant operations.
        """
        # Greet the user
        greeting_message = Greetings()
        # Wish the user based on the time of the day
        wish_message = Make_wish()
        complete_message = f"{greeting_message} {wish_message}"
        Speak_with_script(complete_message)

        # Preprocess Wake_up_commands and Bye_commands
        clean_wake_up_commands = [clean_command(cmd) for cmd in Wake_up_commands]
        clean_bye_commands = [clean_command(cmd) for cmd in Bye_commands]

        while True:
            command = listen().lower()
            clean_user_command = clean_command(command)
            if clean_user_command in clean_wake_up_commands:
                response = random.choice(Wake_up_responses)
                Speak(response)
            elif clean_user_command in clean_bye_commands:
                response = random.choice(Bye_responses)
                Speak(response)
                break
            elif clean_user_command == "stop":
                response = random.choice(Bye_responses)
                Speak(response)
                break
            elif command.startswith(("jarvis","jar","hey","hi","hello","buddy")):
                command = command.replace("jarvis","")
                command = command.replace("jar","")
                command = command.replace("hey","")
                command = command.replace("hi","")
                command = command.replace("hello","")
                command = command.replace("buddy","")
                brain = Brain(command)
                Speak(brain)
            elif command.endswith(("jarvis","jar","buddy")):
                command = command.replace("jarvis","")
                command = command.replace("jar","")
                command = command.replace("buddy","")
                brain = Brain(command)
                Speak(brain)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    Jarvis()