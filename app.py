from flask import Flask, render_template
import requests
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import random

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

app = Flask(__name__)
app.debug = True
URL = "https://www.affirmations.dev/"
# Sample Response: {"affirmation":"The path to success is to take massive, determined action"}


@app.route('/')
def home():
    res = requests.get(url=URL)
    affirmation = res.json()["affirmation"]
    antifirmation = anti(affirmation)
    return render_template("home.html", quote=antifirmation)


def anti(affirmation):
    tokens = word_tokenize(affirmation)
    tagged_tokens = nltk.pos_tag(tokens)

    result = []

    for word, part_of_speech in tagged_tokens:
        replaced_word = word
        if word in ["is", "can", "will"]:
            replaced_word = word + " not"
        elif part_of_speech == "JJ":  # word is an adjective
            antonyms = set()
            for syn in wordnet.synsets(word):
                for lem in syn.lemmas():
                    if lem.antonyms():
                        antonyms.add(lem.antonyms()[0].name())
            if not antonyms:
                replaced_word = get_random_adjective()
            else:
                replaced_word = random.sample(antonyms, 1)
        replaced_word = random_capitalize_word(replaced_word)
        result.append(replaced_word)

    result = " ".join(result)

    return result


def random_capitalize_word(word):
    result = ""
    for char in word:
        if char.isalpha():
            result += random_capitalize(char)
        else:
            result += char
    return result


def random_capitalize(letter):
    if random.random() > 0.5:
        return letter.upper()
    else:
        return letter.lower()


def get_random_adjective():
    url = "https://random-word-form.herokuapp.com/random/adjective"
    res = requests.get(url=url)
    res = res.json()
    return res[0]
