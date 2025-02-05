import datetime
import sys
import os

#Add the root directory to the pyhton  path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Data.Wish_data.Wish_dialog_data import Morning_wishes, Afternoon_wishes, Evening_wishes, Night_wishes
import random

today = datetime.date.today()
formatted_date = today.strftime("%B %d, %Y")
now_x = datetime.datetime.now()


def Make_wish():
    """
    Function to wish the user based on the current time of the day.
    """
    current_time = now_x.hour

    if current_time < 12:
        wish = random.choice(Morning_wishes)
    elif 12 <= current_time < 17:
        wish = random.choice(Afternoon_wishes)
    elif 17 <= current_time < 21:
        wish = random.choice(Evening_wishes)
    else:
        wish = random.choice(Night_wishes)

    message = f"{wish}"
    return message
