# 📰 NewsPulse – Global News Trend Analyzer Using AI

**NewsPulse** is an intelligent web application that delivers **real-time trending news** from around the world, enhanced with **AI-powered analysis and interactive insights**.  
Built with **Flask**, the app integrates **GNews API**, **Google Gemini API**, and **NLP libraries** to analyze sentiment, extract named entities, and visualize global news trends.

---

## 🚀 Features

### 🌍 Global News Fetching
- Uses **GNews API** to fetch top trending news from multiple categories:
  - World  
  - Technology  
  - Business  
  - Sports  
  - Entertainment  
  - Science  
  - Health  

### 🔍 Smart Search
- Search for specific **keywords** or **topics** to view related news stories instantly.

### 💬 AI-Powered Chatbot
- Integrated **Gemini API chatbot** that allows users to:
  - Ask questions related to any article.
  - Get summaries or contextual insights.
  - Explore related global events and trends.

### 😊 Sentiment Analysis
- Analyzes each news article using **TextBlob** to determine:
  - Positive
  - Negative
  - Neutral sentiments  
- Displays sentiment visualizations for better understanding of global mood.

### 🧠 Named Entity Recognition (NER)
- Uses **spaCy** to extract entities such as:
  - People  
  - Organizations  
  - Locations  
- Visualized for interactive analysis.

### 📊 Data Visualizations
- Sentiment distribution graphs.  
- NER statistics and frequency charts.  
- News source representation via charts.

### 🔗 External Links
- Each article includes:
  - **Open Full News** → opens the original source.  
  - **Ask Bot** → allows AI interaction about that news.

---

## 🧰 Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend** | Flask (Python) |
| **Frontend** | HTML, CSS, JavaScript |
| **APIs** | GNews API, Google Gemini API |
| **AI / NLP** | TextBlob, spaCy |
| **Data Handling** | Requests, JSON |
| **Environment Management** | Python-dotenv |
| **Visualization** | Chart.js / Matplotlib (depending on your setup) |

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/newspulse.git
cd newspulse
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

### 3. Activate the Environment
```bash
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Add Environment Variables
```bash
GNEWS_API_KEY=your_gnews_api_key
GEMINI_API_KEY=your_gemini_api_key

```

### 6. Run the App
```bash
python app.py
```

## 📈 Example Visualizations
- Sentiment Pie Chart
- NER Word Frequency Graph
- Source Distribution Bar Chart

## 🧩 Project Structure
```bash
NewsPulse/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   ├── index.html
│   └── login.html
│
├── app.py
├── requirements.txt
├── .env               # (ignored by .gitignore)
└── venv/              # (ignored)
```

## 🔒 Environment & Security
- env file stores all API keys securely.
- gitignore ensures .env and venv/ are not pushed to GitHub.
- Sensitive data is never exposed.

## ⭐ Acknowledgments

This project was made possible thanks to the following technologies and APIs:

- [**GNews API**](https://gnews.io/) — for providing real-time global news data and category-based filtering.  
- [**Google Gemini API**](https://ai.google.dev/) — for powering the intelligent chatbot and AI-driven news insights.  
- [**TextBlob**](https://textblob.readthedocs.io/) — for sentiment analysis and text processing.  
- [**spaCy**](https://spacy.io/) — for advanced natural language processing and named entity recognition (NER).  
- [**Flask**](https://flask.palletsprojects.com/) — for serving as the lightweight web framework that powers the backend.
