import spacy
import os

from pathlib import Path
from transformers import pipeline

classifier = pipeline("sentiment-analysis")


def load_model_output(text):
    """Function to load the trained machine learning model for inference and
    return the output as the necessary entities and topics for each element
    param text: The input text blob being entered by user
    """
    # uncomment when working in linux and remove subsequent two lines
    # nlp = spacy.load("../models/quick-spacy/")
    model_path = Path(__file__).parent.absolute() / "models/quick-spacy/"
    nlp = spacy.load(model_path)
    doc = nlp(text)
    entity = [ent.text for ent in doc.ents]
    labels = [ent.label_ for ent in doc.ents]
    return entity, labels


def analyser(text):
    """
    A input pipeline which returns for a given text blob, output of
    aspect based sentiment analaysis as list of entities with associated
    sentiment.
    Usage:
        >> analyser(text="awesome staff and tea was epic.")
            {'staff': 'pos, 'tea': 'pos'}
    :param text: The input text blob which is being used by model
    :param topics: Optional and update as required
    """

    entity, labels = load_model_output(text)
    print(labels)

    full_sentence = []
    full_text = text.split(".")

    for i in range(len(entity)):
        temp = ""
        for t in full_text:
            if len(full_text) >= 1:
                if entity[i] in t.lstrip():
                    temp += t
        full_sentence.append(temp)

    print(full_sentence)
    results = classifier(full_sentence)
    print(results)
    sentiment_output = {}

    for i, t in enumerate(results):
        print(i, t)
        print(labels[i])
        print(t["label"])
        sentiment_output[labels[i]] = results[i]["label"]

    response = {}

    response["sentiment"] = sentiment_output
    response["staff"] = sentiment_output.get("staff")
    response["facility"] = sentiment_output.get("facility")
    response["location"] = sentiment_output.get("location")
    response["service"] = sentiment_output.get("service")
    response["overall_sentiment"] = overall_sentiment(text)

    return response


def overall_sentiment(text):
    results = classifier(text)
    return results[0]["label"]
