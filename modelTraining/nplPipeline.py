import nltk
nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
import numpy as np

stemmer = PorterStemmer()

def tokenize(str):
    return nltk.word_tokenize(str)


def lower_stemming(str):
    return stemmer.stem(str.lower())

def bag_of_words(tok_str, words):
    idx = 0
    bag = np.zeros(len(words))
    tok_str = [lower_stemming(word) for word in tok_str]
    for word in words:
        if word in tok_str:
            bag[idx] = 1
        idx += 1 
    return bag


str = "Hello world, I am delighted to announce that I work!!"
words = ["Organize", "organizer", "organizing", "organizes"]
stemmed_words = [lower_stemming(word) for word in words]

# print(tokenize(str))
# print(stemmed_words)

sentence = ["hello", "how", "are", "you"]
words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
bag = bag_of_words(sentence, words)
# print(bag)

