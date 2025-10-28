from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from textblob import TextBlob
from collections import Counter
from datetime import datetime
import spacy
from google import genai # NEW: Import the Gemini SDK

# ---------- LOAD MODELS & ENVIRONMENT ----------
load_dotenv() 
nlp = spacy.load("en_core_web_sm") # Load English spaCy model

# API configuration
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "YOUR_GNEWS_API_KEY_HERE")
BASE_URL = "https://gnews.io/api/v4"

# NEW: Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE") 
if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
    print("WARNING: GEMINI_API_KEY not set in .env. Chatbot will use a placeholder response.")
    genai_client = None
else:
    genai_client = genai.Client(api_key=GEMINI_API_KEY)


app = Flask(__name__)
# No SECRET_KEY needed since we removed session management.


# ---------- SENTIMENT ANALYSIS (Unchanged) ----------
def get_sentiment(text):
    """Calculates sentiment and assigns a category and emoji."""
    if not text:
        return {"category": "N/A", "emoji": "⚪"}
    
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.3:
        return {"category": "Positive", "emoji": "😊"}
    elif polarity < -0.3:
        return {"category": "Negative", "emoji": "😞"}
    else:
        return {"category": "Neutral", "emoji": "😐"}


# ---------- FETCH NEWS (Unchanged) ----------
def get_trending_news(category=None, keyword=None):
    """Fetches trending news or searches for news, and adds sentiment."""
    params = {
        "token": GNEWS_API_KEY,
        "lang": "en",
        "max": 100,
    }

    if keyword:
        url = f"{BASE_URL}/search"
        params["q"] = keyword
    else:
        url = f"{BASE_URL}/top-headlines"
        if category:
            params["topic"] = category

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        
        for article in articles:
            sentiment_data = get_sentiment(article.get('description', article.get('title', '')))
            article['sentiment'] = sentiment_data['category']
            article['sentiment_emoji'] = sentiment_data['emoji']
            
        return articles
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


# ---------- NAMED ENTITY RECOGNITION (Unchanged) ----------
def extract_entities(articles):
    """
    Extracts named entities (people, organizations, locations) from news titles and descriptions.
    Returns a dictionary grouped by entity type.
    """
    all_text = " ".join([
        (a.get("title", "") or "") + " " + (a.get("description", "") or "")
        for a in articles
    ])
    
    doc = nlp(all_text)
    
    entity_data = {"PERSON": [], "ORG": [], "GPE": []} # GPE = geopolitical entities (countries, cities)
    
    for ent in doc.ents:
        if ent.label_ in entity_data:
            entity_data[ent.label_].append(ent.text)
    
    # Count top entities for each type
    entity_summary = {
        label: dict(Counter(names).most_common(5))
        for label, names in entity_data.items() if names
    }
    return entity_summary


# ---------- CHATBOT API ENDPOINT (UPDATED) ----------

@app.route("/chatbot", methods=["POST"])
def chatbot_interaction():
    data = request.json
    user_query = data.get("query", "")
    current_url = data.get("url", "") # We can use this to grab article content for context later

    if not user_query:
        return jsonify({"response": "Please ask a question."})

    # Base prompt for the AI's role
    system_instruction = (
        "You are the Newspulse Contextual Guide. You help users understand news jargon and answer questions based on general knowledge. "
        "Keep your answers concise and helpful."
    )

    if genai_client:
        try:
            # Call the Gemini API
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=user_query,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instruction
                )
            )
            gemini_response = response.text
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            gemini_response = "Sorry, I'm having trouble connecting to the AI right now. Please check your API key and connection."
    else:
        # Placeholder response if the API key is missing
        gemini_response = f"Hello! I received your message: '{user_query}'. I am currently running in placeholder mode because the Gemini API key is missing. Please set the GEMINI_API_KEY in your .env file to enable full chat functionality."


    return jsonify({"response": gemini_response})


# ---------- FLASK ROUTES (Unchanged) ----------
@app.route("/", methods=["GET"])
def home():
    news = get_trending_news()
    return render_template("index.html", news=news)

@app.route("/category/<category>")
def category_news(category):
    news = get_trending_news(category=category)
    return render_template("index.html", news=news, selected_category=category)

@app.route("/search", methods=["POST"])
def search_news():
    keyword = request.form.get("keyword")
    news = get_trending_news(keyword=keyword)
    return render_template("index.html", news=news, keyword=keyword)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", selected_category="dashboard")


# ---------- DASHBOARD DATA (Unchanged) ----------
@app.route("/dashboard-data")
def dashboard_data():
    """Aggregates live data from GNews for dashboard visualizations."""
    news = get_trending_news()

    if not news:
        return jsonify({"error": "No news available"}), 500

    # --- 1. Sentiment Counts ---
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for article in news:
        sentiment = article.get("sentiment", "Neutral")
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1

    # --- 2. Source Counts ---
    source_counts = {}
    for article in news:
        source_name = article.get("source", {}).get("name", "Unknown")
        source_counts[source_name] = source_counts.get(source_name, 0) + 1

    # --- 3. Top Keywords ---
    words = []
    for article in news:
        text = (article.get("title", "") + " " + article.get("description", "")).lower()
        for w in text.split():
            if len(w) > 4 and w.isalpha():
                words.append(w)
    top_words = dict(Counter(words).most_common(5))

    # --- 4. Article Volume Over Time ---
    date_counts = {}
    for article in news:
        pub_date = article.get("publishedAt")
        if pub_date:
            try:
                date = datetime.fromisoformat(pub_date.replace("Z", "+00:00")).strftime("%b %d")
                date_counts[date] = date_counts.get(date, 0) + 1
            except Exception:
                pass
    sorted_volume = dict(sorted(date_counts.items(), key=lambda x: x[0]))

    # --- 5. Useful vs Not Useful Ratio ---
    useful_ratio = {
        "useful": sentiment_counts["Positive"] + sentiment_counts["Neutral"],
        "not_useful": sentiment_counts["Negative"]
    }

    # --- 6. Named Entity Recognition ---
    entity_summary = extract_entities(news)

    # Return JSON response
    return jsonify({
        "sentiment": sentiment_counts,
        "sources": source_counts,
        "topics": top_words,
        "volume": sorted_volume,
        "useful": useful_ratio,
        "entities": entity_summary
    })


# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(debug=True)