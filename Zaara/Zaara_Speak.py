import sys
import threading
import os
import time
import pyttsx3
from textblob import TextBlob

def Detect_Emotion(text):
    text_lower = text.lower()

    # Keywords for different feelings
    ecstatic_keywords = ['ecstatic']
    overjoyed_keywords = ['overjoyed']
    elated_keywords = ['elated']
    joyful_keywords = ['joyful']
    happy_keywords = ['happy']
    cheerful_keywords = ['cheerful']
    content_keywords = ['content']
    pleased_keywords = ['pleased']
    neutral_keywords = ['neutral']
    indifferent_keywords = ['indifferent']
    unhappy_keywords = ['unhappy']
    sad_keywords = ['sad']
    mournful_keywords = ['mournful']
    despondent_keywords = ['despondent']
    melancholy_keywords = ['melancholy']
    depressed_keywords = ['depressed']
    devastated_keywords = ['devastated']
    hopeful_keywords = ['hopeful']
    optimistic_keywords = ['optimistic']
    grateful_keywords = ['grateful']
    inspired_keywords = ['inspired']
    amused_keywords = ['amused']
    calm_keywords = ['calm']
    confused_keywords = ['confused']
    disappointed_keywords = ['disappointed']
    frustated_keywords = ['frustated']
    anxious_keywords = ['anxious']
    overwhelmed_keywords = ['overwhelmed']
    guilty_keywords = ['guilty']
    disgusted_keywords = ['disgusted']
    repulsed_keywords = ['repulsed']
    detached_keywords = ['detached']
    confident_keywords = ['confident']
    
    # Check for each emotion

    if any(word in text_lower for word in ecstatic_keywords):
       return "ecstatic"
    elif any(word in text_lower for word in overjoyed_keywords):
        return "overjoyed"
    elif any(word in text_lower for word in elated_keywords):
        return "elated"
    elif any(word in text_lower for word in joyful_keywords):
        return "joyful"
    elif any(word in text_lower for word in happy_keywords):
        return "happy"
    elif any(word in text_lower for word in cheerful_keywords):
        return "cheerful"
    elif any(word in text_lower for word in content_keywords):
        return "content"
    elif any(word in text_lower for word in pleased_keywords):
        return "pleased"
    elif any(word in text_lower for word in neutral_keywords):
        return "neutral"
    elif any(word in text_lower for word in indifferent_keywords):
        return "indifferent"
    elif any(word in text_lower for word in unhappy_keywords):
        return "unhappy"
    elif any(word in text_lower for word in sad_keywords):
        return "sad"
    elif any(word in text_lower for word in mournful_keywords):
        return "mournful"
    elif any(word in text_lower for word in despondent_keywords):
        return "despondent"
    elif any(word in text_lower for word in melancholy_keywords):
        return "melancholy"
    elif any(word in text_lower for word in depressed_keywords):
        return "depressed"
    elif any(word in text_lower for word in devastated_keywords):
        return "devastated"
    elif any(word in text_lower for word in hopeful_keywords):
        return "hopeful"
    elif any(word in text_lower for word in optimistic_keywords):
        return "optimistic"
    elif any(word in text_lower for word in amused_keywords):
        return "amused"
    elif any(word in text_lower for word in calm_keywords):
        return "calm"
    elif any(word in text_lower for word in confused_keywords):
        return "confused"
    elif any(word in text_lower for word in disappointed_keywords):
        return "disappointed"
    elif any(word in text_lower for word in frustated_keywords):
        return "frustated"
    elif any(word in text_lower for word in anxious_keywords):
        return "anxious"
    elif any(word in text_lower for word in overwhelmed_keywords):
        return "overwhelmed"
    elif any(word in text_lower for word in guilty_keywords):
        return "guilty"
    elif any(word in text_lower for word in disgusted_keywords):
        return "disgusted"
    elif any(word in text_lower for word in repulsed_keywords):
        return "repulsed"
    elif any(word in text_lower for word in detached_keywords):
        return "detached"
    elif any(word in text_lower for word in grateful_keywords):
        return "grateful"
    elif any(word in text_lower for word in inspired_keywords):
        return "inspired"
    elif any(word in text_lower for word in confident_keywords):
        return "confident"
    else:
        # If no emotions are detected
        return "unknown"

def Get_Emotion(sentiment):
    if sentiment > 0.7:
        return "ecstatic", (220, 1.5)
    elif 0.6 <= sentiment <= 0.7:
        return "overjoyed", (180, 1.4)
    elif 0.5 <= sentiment < 0.6:
        return "elated", (190, 1.3)
    elif 0.5 <= sentiment < 0.6:
        return "angry", (290, 1.3)
    elif 0.4 <= sentiment < 0.5:
        return "joyful", (180, 1.2)
    elif 0.3 <= sentiment < 0.4:
        return "happy", (170, 1.1)
    elif 0.2 <= sentiment < 0.3:
        return "cheerful", (160, 1.0)
    elif 0.1 <= sentiment < 0.2:
        return "content", (150, 0.9)
    elif 0.05 <= sentiment < 0.1:
        return "pleased", (140, 0.8)
    elif -0.05 <= sentiment < 0.05:
        return "neutral", (130, 1)
    elif -0.1 <= sentiment -0.05:
        return "indifferent", ( 120, 1)
    elif -0.2 <= sentiment < -0.1:
        return "unhappy", (110, 1)
    elif -0.3 <= sentiment < -0.2:
        return "sad", ( 100, 1)
    elif -0.4 <= sentiment < -0.3:
        return "mournful", (100, 1)
    elif -0.5 <= sentiment < -0.4:
        return "despondent", (170, 1)
    elif -0.6 <= sentiment < -0.5:
        return "melancholy", (170, 0.1)
    elif -0.7 <= sentiment < -0.6:
        return "depressed", (60, 1)
    elif sentiment <= -0.7:
        return " devastated", ( 180, 1)
    elif 0.5 <= sentiment < 0.6:
        return "hopeful", (175, 1.3)
    elif 0.4 <= sentiment < 0.5:
        return "optimistic", (165, 1.1)
    elif 0.3 <= sentiment < 0.4:
        return "grateful", (155, 1.1)
    elif 0.2 <= sentiment < 0.3:
        return "inpired", (145, 1.0)
    elif 0.1 <= sentiment < 0.2:
        return "amused", (135, 0.9)
    elif 0.05 <= sentiment < 0.1:
        return "clam", (125, 0.8)
    elif -0.05 <= sentiment < 0.05:
        return"confused", (115, 0.8)
    elif -0.1 <= sentiment < -0.05:
        return "disappointed", (105, 0.9)
    elif -0.2 <= sentiment < -0.1:
        return "frustated", (100, 0.5)
    elif -0.3 <= sentiment < -0.2:
        return "anxious", (85, 0.8)
    elif -0.4 <= sentiment < -0.3:
        return "overwhelmed", (100, 1)
    elif -0.5 <= sentiment < -0.4:
        return "guilty", (100, 1)
    elif -0.6 <= sentiment < -0.5:
        return "disgusted", (100, 1)
    elif -0.2 <= sentiment < -0.6:
        return "repulsed", (100, 1)
    elif sentiment <= -0.7:
        return "detached", (150, 0.8)

    # Add more emotions if needed.

def Track_emotion_phrases(text):
    if any(word in text.lower() for word in ['love', 'romance', 'affection', 'passion', 'adoration', 'devotion', 'warmth', 'amour', 'infatuation', 'desire', 'attraction', 'yearning', 'admiration', 'enchantment', 'sweetheart', 'heartfelt', 'tender', 'embrace', 'cherish', 'butterfly', 'sweetness', 'amorous', 'sentiment', 'woo', 'hug', 'kiss', 'whisper', 'yearn', 'lovers', 'connection', 'affinity', 'lovers', ' magnetic', 'attracted', 'heartwarming', 'softness', 'attachmnet', 'admirer', 'heartthrob', 'beloved', 'emotion', 'fond', 'harmony', 'sympathy', 'infatuated', 'enamored', 'darling', 'tenderly', 'swoon', 'entranced', 'enveloped', 'heartfell', 'heartstrings', 'enamored', 'lovestruck', 'warmhearted', 'companionate', 'quioxtic', 'wooing', 'nurturing', 'statgazing', 'whispers', 'languishing', 'romeo', 'juliet', 'emblazoned', 'fancy', 'allure', 'rapture', 'yearning', 'enraptured', 'yearning', 'longing', 'alluring', 'savor', 'spark', 'elation']):
        return "love"

    elif any(word in text.lower() for word in ['happy', 'joyful', 'pleased', 'content', 'cheerful', '']):
        return "happy"
