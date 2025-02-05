''' This file contains Speaking abilities for jarvis'''

import asyncio
import threading
import os
import sys
import edge_tts # Edge TTS library for text-to-speech
import pygame   # Pygame for audio playback

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Brain import Print_Animated_Message

# Define the voice for TTS (using Edge TTS voices)
voice = "en-CA-ClaraNeural"
buffer_size = 1024 # Buffer size for reading files

def Remove_file(file_path):
    """
    Attempts to remove the specified file. Retries up to three times if an error occurs.
    
    Args:
        file_path (str): The path to the file to be removed.
    """
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            with open(file_path,"wb"):
                pass # Open file to ensure it is not in use
            os.remove(file_path)
            break
        except Exception as e:
            print(f"An unexpected error occurred while removing the file: {e}")
            attempts += 1


async def Speech_Generator(text, output_file)->None:
    """
    Asynchronously generates speech from the provided text and saves it to an output file.
    Plays the audio after it has been saved.
    
    Args:
        text (str): The text to be converted to speech.
        output_file (str): The path to the output file where the speech will be saved.
    """
    try:
        # Generate speech using Edge TTS and save to output file
        communicated_text = edge_tts.Communicate(text,voice)
        await communicated_text.save(output_file)
        # Play the generated audio in a separate thread
        thread = threading.Thread(target= Play_audio, args= (output_file,))
        thread.start()
        thread.join()
    except Exception as e:
        print(f"An unexpected error occurred in amain function: {e}")
    finally:
        Remove_file(output_file) # Remove the output file after playback

def Play_audio(file_path):
    """
    Plays the specified audio file using Pygame.
    
    Args:
        file_path (str): The path to the audio file to be played.
    """
    try:
        pygame.init()                       # Initialize Pygame
        pygame.mixer.init()                 # Initialize Pygame mixer for audio
        pygame.mixer.music.load(file_path)  # Load the audio file
        pygame.mixer.music.play()           # Play the loaded audio file

        # Keep checking if the audio is still playing
        while pygame.mixer.music.get_busy():
            pygame.time.delay(10)

        pygame.mixer.music.stop() # Stop audio playback
        pygame.mixer.quit()       # Quit the mixer
    except Exception as e:
        print(f"An unexpected error occurred while playing the audio: {e}")


def Speak(text, output_file = None):
    """
    Converts text to speech and plays the audio.

    Args:
        text (str): The text to be converted to speech.
        output_file (str, optional): The path to save the audio file. Defaults to "speak.mp3" in the current directory.
    """
    # Set default output file if none is provided
    if output_file is None:
        output_file = f"{os.getcwd()}/speak.mp3"
        asyncio.run(Speech_Generator(text, output_file)) # Set default output file if none is provided

def Speak_with_script(message):
    Speak_thread = threading.Thread(target= Speak, args=(message,))
    Script_thread = threading.Thread(target= Print_Animated_Message, args=(message,))

    Speak_thread.start()
    Script_thread.start()

    Speak_thread.join()
    Script_thread.join()
