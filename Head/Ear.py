''' This file contains listening abilities for jarvis'''

import speech_recognition as sr # Speech Recognition package for recognizing the command given from the user
import os                       # OS module for operatong system maanagement
import threading                # Threading for faster code execution
from mtranslate import translate# Translating text from hindi to english
import colorama                 # For style and Animation
import pyaudio
# from Head.Mouth import Speak

colorama.init(autoreset = True) # Reseting style after each print

stop_threads = False  # for handling the threads

def Print_Loop_Animation():
    """
    This function is created for reseting the style after each print.
    """
    while not stop_threads:
        print(colorama.Fore.LIGHTGREEN_EX + " I am Listening........", end= "", flush= True)
        print(colorama.Style.RESET_ALL, end= "", flush= True)
        print("", end= "", flush= True)

def Translate_Hindi_to_English(text):
    """
    This function will translate the command into english if user speaks in hindi,
    if user is already speaking in english then it's okay

    Args:
        text(str): The text which will be translated into english.
    """
    Translated_text = translate(text, to_language= "en-in",from_language= "hi") # This line will translate speech hindi to english 
    return Translated_text

def listen():
    """
    This is the major function of this file because it will listen what user is saying.
    """
    global stop_threads
    recognizer = sr.Recognizer()                # Setting up the recognizer using Recognizer() class so that it can recognize the command
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 35000           # It will set maximum energy to speak
    recognizer.dynamic_energy_adjustment_damping = 0.02 # How quickly the recognizer’s energy threshold adapts to changes in background noise.
    recognizer.dynamic_energy_ratio = 1.0       # This ratio determines the multiplier used to set the energy threshold relative to the observed background noise.
    recognizer.pause_threshold = 0.5            # It is used to tell jarvis that how long can user take pause while speking in between
    recognizer.non_speaking_duration = 0.1    # This will determine the non speaking durantion of the user if user don't speak in this duration then control will move forward.
    recognizer.operation_timeout = None         # It will set the operation timeout that means it will tell jarvis then how long the recognizer can operate
    recognizer.pause_threshold = 0.2            # It is used to tell jarvis that how long can user take pause while speking in between
    recognizer.quiet_duration = 0.3             # This will set the quiet duration of the recognizer
   

    with sr.Microphone() as source:             # Initializing microphone using Microphone() class.
        recognizer.adjust_for_ambient_noise(source) # Noise cancellation
        while not stop_threads:
            print(colorama.Fore.LIGHTBLUE_EX + "I am listening......Speak now!", end= "", flush= True)
            try:
                audio = recognizer.listen(source,timeout= None) # This line helps jarvis to listen
                print("\r" + colorama.Fore.LIGHTYELLOW_EX + "Please wait! Recognizing.........", end= "", flush= True)
                recognized_text = recognizer.recognize_google(audio).lower() # Recognizer user recognize_google function to recognize what user said.
                if recognized_text:
                    translated_text = Translate_Hindi_to_English(recognized_text) # Translating command into english if it is in hindi.
                    os.system("cls" if os.name == "nt" else "clear") # Clearing the console
                    print("\n" + "Mr Aditya: " + translated_text, end= "\n")
                    return translated_text
                else:
                    recognized_text = ""
            except sr.UnknownValueError: # Exception if jarvis didn't get the command
                print("\rCould not understand audio, please try again.", flush=True)
                recognized_text = ""
            except sr.WaitTimeoutError: # Exception if no command is given. Time out error
                print("\rListening timed out, please try again.", flush=True)
            except sr.RequestError:
                print("\r Recogintion connection failed! Please check internet connection")
            finally:
                if stop_threads:
                    break
                print("\r", end= "", flush= True)
        # os.system("cls" if os.name == "nt" else "clear")                    # Clearing the console
        # try:
        #     listen_thread = threading.Thread(target= listen)                # Threading the listen() function for faster execution
        #     print_thread = threading.Thread(target= Print_Loop_Animation)   # Threading the Print_Loop_Animation() function for faster execution
        #     listen_thread.start()                                           # Starting the listen_thread
        #     print_thread.start()                                            # Starting the print_thread
        #     listen_thread.join()                                            # Joining the listen_thread
        #     stop_threads = False
        #     print_thread.join()                                             # Joining the print_thread
        # except KeyboardInterrupt: 
        #     stop_threads = True                                             # Exception case is keyboard inturruption happens

# Testing the listen() function
# while True:
#     command = listen().lower()
#     if command == "stop":
#         break
#     else:
#         pass