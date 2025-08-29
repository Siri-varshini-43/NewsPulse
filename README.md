# 📰 NewsPulse – Global News Trend Analyzer Using AI

NewsPulse is an **AI-powered finance news dashboard** built with **Streamlit**.  
It classifies financial news into categories (Stock Market, Cryptocurrency, Banking, Economy), analyzes sentiment (Positive, Negative, Neutral), and extracts named entities (People, Organizations, Locations).  
The dashboard provides visual insights such as word clouds, sentiment distribution, and trending entities to help users quickly understand financial news trends.  

---

## 🚀 Features
- **Rule-based Categorization** – Classifies news into:
  - 📈 Stock Market  
  - 💰 Cryptocurrency  
  - 🏦 Banking  
  - 🌍 Economy  
  - 📂 Others  
  - 🔎 All Categories  
- **Sentiment Analysis** – Uses a pre-trained transformer model to detect **Positive / Negative / Neutral** sentiment.  
- **Named Entity Recognition (NER)** – Extracts **people, organizations, and locations** from articles.  
- **Filters & Search** – Search by keyword or filter by category.  
- **Visualizations** –  
  - Category distribution chart  
  - WordCloud of trending terms  
  - Sentiment pie chart  
  - Top named entities  
- **Latest News Section** – Shows the most recent finance-related articles.  

---

## 🛠️ Tech Stack
- **Frontend & Dashboard:** [Streamlit](https://streamlit.io/)  
- **Data Handling:** Pandas  
- **Visualization:** Matplotlib, WordCloud  
- **NLP Models:**  
  - Hugging Face Transformers (for sentiment)  
  - spaCy (for NER)  
- **Data Source:** Finance news dataset (`finance_news_cleaned.csv`)  

---

## 📂 Project Structure
```bash
NewsPulse/
│── finance_news_cleaned.csv        # Raw dataset
│── finance_news_classified.csv     # Processed dataset with categories, sentiment & entities
│── finance_news_raw.csv            # Original collected dataset
│── data_fetch.py                   # Script to fetch news
│── preprocess.py                   # Script to clean & preprocess data
│── classify.py                     # Script for classification & preprocessing
│── dashboard.py                    # Streamlit dashboard
│── README.md                       # Project documentation
```




## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/newspulse.git
   cd newspulse
   ```

2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install streamlit pandas matplotlib wordcloud spacy transformers torch scikit-learn
   ```

3. **Download spaCy English model**
   ```bash
    python -m spacy download en_core_web_sm
   ```

4. **Run the project**
   ```bash
   python data_fetch.py
   python preprocess.py
   python classify.py
   Python -m streamlit run dashboard.py
   ```
