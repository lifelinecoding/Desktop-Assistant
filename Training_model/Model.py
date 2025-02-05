#Import inbuild packages
import sys
import os
#Add the root directory to the pyhton  path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#Import necessary libraries for NLP and ML
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
import numpy as np

#Import custom modules for voice interaction
from Head.Mouth import Speak
from Head.Ear import listen

#Download necessary NLTK data files
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')

#Function to load the QnA dataset from a text file
def Load_dataset(file_path):
    """
    Load the dataset from a specified text file.
    Each line in the file should contain a question and answer separated by a colon (:).

    Args:
        file_path (str): Path to the QnA data file.

    Returns:
        list: A list of dictionaries with 'question' and 'answer' pairs.
    """

    with open(file_path, 'r', encoding= 'utf-8') as file:
        lines = file.readlines()
        qna_pairs = [line.strip().split(':',1) for line in lines if ':' in line]
        dataset = [{'question': q, 'answer': a} for q,a in qna_pairs]
        #print("Loaded Dataset:", dataset)

    return dataset


#Function to preprocess text by removing stopwords and lemmatizing tokens
def Preprocessor_of_text(text):
    """
    Preprocess the input text by tokenizing, removing stopwords, and lemmatizing.

    Args:
        text (str): The input text to preprocess.

    Returns:
        str: Preprocessed and cleaned text.
    """

    # Customize stop words to retain essential question words
    stop_words = set(stopwords.words('english')) -{"what", "is","can","how","are", "you"}  #This converts the list of stopwords into a set. A set is used because it allows faster lookup operations (compared to a list). This subtracts a custom set of words from the default stop words.
    stop_words.add("who")  # Add custom stop words as needed
    lemmatizer = WordNetLemmatizer()        #This initializes the WordNet Lemmatizer. It's a process that reduces words to their base or dictionary form (e.g., "running" → "run", "better" → "good").

    # Tokenize and preprocess text
    tokens = word_tokenize(text.lower())        #This splits the text into individual words or tokens after converting the text into lower case
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]   #Each token is lemmatized (converted to its base form) and filtered out non-alphanumeric tokens (like punctuation or special characters).
    return ' '.join(tokens)

#Function to train the TF-IDF vectorizer on the dataset
def Train_tdidf_vectorizer(dataset):
    """
    Train a TF-IDF vectorizer on the questions in the dataset.

    Args:
        dataset (list): List of question-answer pairs.

    Returns:
        tuple: A trained TfidfVectorizer and its transformed matrix.
    """

    corpus = [Preprocessor_of_text(qa['question']) for qa in dataset]   #This line creates a list of preprocessed questions (called the corpus) from the dataset.
    vectorizer = TfidfVectorizer()              #This initializes a TF-IDF (Term Frequency - Inverse Document Frequency) Vectorizer from sklearn. It converts the text (questions) into numerical vectors that represent how important a word is in a given document relative to the entire corpus.
    X = vectorizer.fit_transform(corpus)        #This line trains the TF-IDF vectorizer on the corpus and transforms the text data into numerical vectors.
    return vectorizer, X

#Function to retrieve the most relevant answer for a given question
def Get_answer(question, vectorizer, X, dataset):
    """
    Retrieve the most relevant answer by comparing the input question to the dataset.

    Args:
        question (str): User's question.
        vectorizer (TfidfVectorizer): Pre-trained TF-IDF vectorizer.
        X (sparse matrix): Transformed matrix of questions from the dataset.
        dataset (list): List of question-answer pairs.

    Returns:
        str: The most relevant answer or a fallback response if no match is found.
    """
    #Preprocess the input question
    question = Preprocessor_of_text(question)
    question_vec = vectorizer.transform([question])
    #print("Preprocessed Question:", question)

    #Calculate cosine similarity between input and dataset questions
    similarities = cosine_similarity(question_vec, X).flatten()
    #print("Similarities Array:", similarities)  # Debugging
    
    #Handle cases where no similarities are found
    if similarities.size == 0:
        return None
    
    #Find the best match
    best_match_index = similarities.argmax()
    
    #Tighten similarity threshold (adjust to tune performance)
    if similarities[best_match_index] < 0.7:  # Adjust threshold as needed
        return None
    
    # Additional check for token overlap
    best_match_question = dataset[best_match_index]['question']
    input_tokens = set(question.split())
    match_tokens = set(best_match_question.split())
    overlap_ratio = len(input_tokens & match_tokens) / len(input_tokens)

    # Reject if overlap is below 50%
    if overlap_ratio < 0.5:
        return None
    
    #Return the most relevant answer
    return dataset[best_match_index]['answer']


#Main function to handle user queries and respond using text-to-speech
def mind(text):
    """
    Process the user's input, retrieve the most relevant answer, and use TTS to respond.

    Args:
        text (str): User's question.
    """

    #Path to the QnA data file
    data_set_path = r"C:\Users\apate\OneDrive\Desktop\Jarvis Desktop AI\Data\Brain_data\Qna_data.txt"

    # Load the dataset
    dataset = Load_dataset(data_set_path)

    #Train the vectorizer and transform the dataset
    vectorizer , X = Train_tdidf_vectorizer(dataset)
    user_question = text

    #Retrieve and speak the answer
    answer = Get_answer(user_question, vectorizer, X, dataset)
    # Speak(answer)               Written for Debugging
    return answer

#Clear console and start interactive loop for user input
os.system("cls" if os.name == "nt" else "clear")

#Debugging code to test the model
# while True:
#     user_input = input()
#     mind(user_input)
    