import pandas as pd
from transformers import pipeline
import spacy

# ---------------------------
# Rule-based categorization
# ---------------------------
def categorize(text):
    text = str(text).lower()

    stock_keywords = [
    'stock', 'market', 'shares', 'equity', 'nasdaq', 'dow jones', 's&p',
    'ipo', 'dividend', 'earnings', 'valuation', 'bull market', 'bear market',
    'index', 'futures', 'options', 'etf', 'mutual fund', 'trading', 'brokerage'
    ]

    crypto_keywords = [
        'crypto', 'cryptocurrency', 'bitcoin', 'ethereum', 'blockchain',
        'altcoin', 'token', 'defi', 'nft', 'stablecoin', 'wallet',
        'smart contract', 'mining', 'staking', 'exchange', 'ledger',
        'metaverse', 'airdrops', 'tokenomics'
    ]

    banking_keywords = [
        'bank', 'loan', 'mortgage', 'interest rate', 'credit', 'debit',
        'deposit', 'withdrawal', 'overdraft', 'savings account',
        'checking account', 'wire transfer', 'atm', 'capital adequacy',
        'lending', 'branch', 'regulation', 'compliance', 'bankruptcy'
    ]

    economy_keywords = [
        'economy', 'gdp', 'inflation', 'unemployment', 'recession',
        'fiscal', 'monetary', 'policy', 'central bank', 'stimulus',
        'trade deficit', 'exports', 'imports', 'tariff', 'subsidy',
        'sovereign debt', 'currency', 'exchange rate', 'foreign reserves',
        'consumer spending', 'housing market'
    ]


    if any(word in text for word in stock_keywords):
        return 'Stock Market'
    elif any(word in text for word in crypto_keywords):
        return 'Cryptocurrency'
    elif any(word in text for word in banking_keywords):
        return 'Banking'
    elif any(word in text for word in economy_keywords):
        return 'Economy'
    else:
        return 'Other'


# ---------------------------
# Sentiment Analysis (3-class model)
# ---------------------------
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def get_sentiment(text):
    if not text or str(text).strip() == "":
        return "Neutral"

    result = sentiment_pipeline(text[:512])[0]
    label = result["label"]
    
    # Standardize the labels to ensure consistent output
    if "positive" in label.lower():
        return "Positive"
    elif "negative" in label.lower():
        return "Negative"
    else:
        return "Neutral"


# ---------------------------
# Named Entity Recognition (NER)
# ---------------------------
nlp = spacy.load("en_core_web_sm")

def get_entities(text):
    """
    Extracts named entities (Person, Organization, Location) from text.
    Returns them as a comma-separated string.
    """
    if not text or str(text).strip() == "":
        return ""

    doc = nlp(text)
    entities = [f"{ent.text} ({ent.label_})" for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE"]]

    return ", ".join(entities) if entities else ""


# ---------------------------
# Main Script
# ---------------------------
if __name__ == "__main__":
    df = pd.read_csv("finance_news_cleaned.csv")

    # Apply all analyses
    df["category"] = df["clean_content"].apply(categorize)
    df["sentiment"] = df["clean_content"].apply(get_sentiment)  # <-- clean labels
    df["entities"] = df["clean_content"].apply(get_entities)

    # Save classified dataset
    df.to_csv("finance_news_classified.csv", index=False)
    print("✅ Data classified with categories, sentiment, and entities → saved to finance_news_classified.csv.")