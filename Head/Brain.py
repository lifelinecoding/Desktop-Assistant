import threading                        # Importing the threading module to run multiple tasks concurrently
import sys                              # Importing the sys module to access system-specific parameters and functions
import time                             # Importing the time module to add delays
import os                               # Importing the os module to interact with the operating system


# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import webbrowser                       # Importing the webbrowser module to open the search results in a web browser
from wikipedia import wikipedia         # Importing the wikipedia module to search for information on Wikipedia
from Training_model.Model import mind   # Importing the mind function from the Model module to fetch responses from the trained model
from Head.Mouth import Speak            # Importing the Speak function from the Mouth module to convert text to speech

#Function to load question-answer pairs from a file into a dictionary
def Load_qna_data(file_path):
    """
    Load question-answer pairs from the specified file into a dictionary.

    Args:
        file_path (str): Path to the QnA file.

    Returns:
        dict: A dictionary with questions as keys and answers as values.
    """

    Qna_dict = {}
    try:
        with open(file_path, "r", encoding= "utf-8", errors= "replace") as f:
            for line in f:
                line = line.strip() # Remove leading/trailing whitespaces
                if not line:        # Skip empty lines
                    continue
                #Split each line into question and answer
                Parts = line.split(":", 1)
                if len(Parts) != 2:                 # Skip malformed lines
                    print(f"Skipping malformed line: {line}")
                    continue
            Question, Answers = Parts
        Qna_dict[Question.strip()] = Answers.strip()
        
    except FileNotFoundError:
        print(f"An error occurred: File not found {file_path}")
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")

    return Qna_dict

#Lock to ensure thread-safe file operations
lock = threading.Lock()

#Function to save new question-answer pairs to the file
def Save_qna_data(file_path, Qna_dict):
    """
    Save new question-answer pairs to the QnA file without duplicating existing entries.

    Args:
        file_path (str): Path to the QnA file.
        Qna_dict (dict): Dictionary containing question-answer pairs to be saved.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        existing_data = f.read().splitlines()  # Read lines and remove newline characters

    # Create a set of existing questions for quick lookup
    existing_questions = set(line.split(":", 1)[0].strip() for line in existing_data if ":" in line)

    # Open the file in append mode to add new entries
    with open(file_path, "a", encoding="utf-8") as f:
        for Question, Answers in Qna_dict.items():
            if Question not in existing_questions:  # Check if the question already exists
                f.write(f"{Question}:{Answers}\n")  # Append only new entrie


#Path to the QnA data file
Qna_file_path = r"C:\Users\apate\OneDrive\Desktop\Jarvis Desktop AI\Data\Brain_data\Qna_data.txt"
Qna_dict = Load_qna_data(Qna_file_path)


# Function to print a message with an animated typing effect
def Print_Animated_Message(message):
    """
    Print a message character by character with a delay for an animated effect.

    Args:
        message (str): Message to be printed.
    """

    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.095) #Adjust the sleep duration for the animation speed.
    print()


#Function to search for information on Wikipedia
def Wikipedia_Search(prompt):
    """
    Search Wikipedia for the given prompt and respond with a summary.

    Args:
        prompt (str): User query to search on Wikipedia.

    Returns:
        str: Wikipedia summary or None if an error occurs.
    """

    search_prompt = prompt.replace('jarvis', '')
    search_prompt = search_prompt.replace('wikipedia', '')

    Wikipedia_summary = wikipedia.summary(search_prompt,sentences = 2) #Get a summary of the search prompt
    try:
        Animate_thread = threading.Thread(target= Print_Animated_Message, args= (Wikipedia_summary,))
        Speak_thread = threading.Thread(target= Speak, args= (Wikipedia_summary,))

        Animate_thread.start()
        Speak_thread.start()

        Animate_thread.join()
        Speak_thread.join()

        #Save the new question-answer pair
        Qna_dict[search_prompt] = Wikipedia_summary
        Save_qna_data(Qna_file_path, Qna_dict)

    except wikipedia.DisambiguationError:
        Speak("There is an disambiguation page for the given query. Please provide more specific imformation.")
        print("There is an disambiguation page for the given query. Please provide more specific imformation.")
        return None
    except wikipedia.PageError:
        Google_search(prompt)
    except Exception as e:
        Speak(f"An error occurred while searching Wikipedia: {e}")
        print(f"An error occurred while searching Wikipedia: {e}")
        return None
    return Wikipedia_summary

#Function to search Google for the query if Wikipedia fails
def Google_search(query):
    """
    Search Google for the given query and open the results in a web browser.

    Args:
        query (str): User query to search on Google.
    """

    query = query.replace("who is", " ")
    query = query.strip()

    if query:
        url = "https://www.google.com/search?q=" + query
        webbrowser.open_new_tab(url)
        Speak("You can see search results on " + query + " in google on your screen")
        #Commenting out the speak fuction as it is not provided here.
        print("You can see search results on " + query + " in google on your screen")

    else:
        Speak("I didn't catch what you said.")
        #Commenting out the speak fuction as it is not provided here.
        print("I didn't catch what you said.")


# Main function to handle user queries and respond using text-to-speech
def Brain(text):
    """
    Process the user's input, fetch answers from the model, Wikipedia, or Google, and respond.

    Args:
        text (str): User input/query.
    """

    try:
        
        response = mind(text)       # Fetch response from the trained model
        if not response:
            response = Wikipedia_Search(text)       # Search Wikipedia if no response from the model
            if not response:
                Google_search(text)                 # Search Google if Wikipedia fails
            return
        
        #Start animation and speaking concurrently

        Animation_thread = threading.Thread(target= Print_Animated_Message, args= (response,))
        Speak_thread = threading.Thread(target= Speak, args= (response,))

        Animation_thread.start()
        Speak_thread.start()

        Animation_thread.join()
        Speak_thread.join()

        #Assuming "search prompt is defined somewhere"
    except Exception as e:
        print(f"An error occured: {e}")
        Google_search(text)                 # Search Google if Wikipedia fails
