import pandas as pd
import re
import nltk
import spacy
from nltk.corpus import stopwords

# Download stopwords once
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load SpaCy English model (make sure to run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])  
# disabling parser/ner makes it faster for preprocessing

def clean_text(text):
    """
    Cleans and preprocesses text:
    - Removes URLs, non-alphabetic chars
    - Lowercases text
    - Tokenizes using spaCy
    - Removes stopwords
    - Lemmatizes tokens (gets base form of words)
    """
    if not text:
        return ''

    # Remove URLs
    text = re.sub(r"http\S+", "", text)

    # Keep only letters and spaces
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Lowercase
    text = text.lower().strip()

    # Use spaCy for tokenization + lemmatization
    doc = nlp(text)
    tokens = [
        token.lemma_ for token in doc
        if token.lemma_ not in stop_words and len(token.lemma_) > 2
    ]

    return " ".join(tokens)


if __name__ == "__main__":
    # Load raw data
    df = pd.read_csv("finance_news_raw.csv")

    # Apply cleaning
    df["clean_content"] = df["content"].apply(clean_text)

    # Save cleaned data
    df.to_csv("finance_news_cleaned.csv", index=False)
    print("Data cleaned, lemmatized, and saved to finance_news_cleaned.csv.")
