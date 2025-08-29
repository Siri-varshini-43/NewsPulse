import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime, timedelta
from collections import Counter

st.set_page_config(page_title='Finance News Dashboard', layout='wide')
st.title('📊 Finance News Dashboard')

# ---------------------------
# Load data
# ---------------------------
df = pd.read_csv('finance_news_classified.csv')

# Convert UTC to IST
def convert_to_ist(utc_time_str):
    try:
        utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
        ist_time = utc_time + timedelta(hours=5, minutes=30)
        return ist_time.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return utc_time_str

if 'publishedAt' in df.columns:
    df['publishedAt_IST'] = df['publishedAt'].apply(convert_to_ist)

# ---------------------------
# Sidebar filters
# ---------------------------
st.sidebar.header('Filters')
keyword = st.sidebar.text_input('Enter a keyword')
category = st.sidebar.selectbox('Select Category', ['All'] + df['category'].unique().tolist())

# Filter data
filtered_df = df.copy()
if keyword:
    filtered_df = filtered_df[filtered_df['clean_content'].str.lower().str.contains(keyword.lower(), na=False)]

    if filtered_df.empty:
        st.warning("⚠️ No news found related to this keyword or it's not finance-related.")
        st.stop()

if category != 'All':
    filtered_df = filtered_df[filtered_df['category'] == category]

# ---------------------------
# Latest news
# ---------------------------
st.subheader('📰 Latest Trending News')
if 'publishedAt_IST' in filtered_df.columns:
    latest = filtered_df.sort_values('publishedAt_IST', ascending=False).head(5)
else:
    latest = filtered_df.head(5)

if latest.empty:
    st.info("No news available for the selected filters.")
else:
    for _, row in latest.iterrows():
        st.markdown(f"**[{row['title']}]({row['url']})** — *{row['source']}* ({row.get('publishedAt_IST', '')[:10]})")

# ---------------------------
# Visualizations
# ---------------------------
st.subheader('📈 Visualizations')
col1, col2, col3 = st.columns([1, 1, 1])

# Category distribution
with col1:
    st.markdown("**Category Distribution**")
    if not filtered_df.empty:
        st.bar_chart(filtered_df['category'].value_counts())
    else:
        st.info("No data for category chart.")

# Wordcloud
with col2:
    st.markdown("**WordCloud**")
    text = ' '.join(filtered_df['clean_content'].dropna())
    if text:
        wc = WordCloud(width=400, height=250, background_color='white').generate(text)
        st.image(wc.to_array(), use_container_width=True)
    else:
        st.info("No content for wordcloud.")

# Sentiment distribution
# Sentiment distribution
with col3:
    st.markdown("**Sentiment Distribution**")
    if not filtered_df.empty and 'sentiment' in filtered_df.columns:
        # Normalize sentiment labels
        sentiment_map = {
            'positive': 'Positive',
            'negative': 'Negative',
            'neutral': 'Neutral',
            1: 'Positive',
            -1: 'Negative',
            0: 'Neutral'
        }
        filtered_df['sentiment_normalized'] = filtered_df['sentiment'].map(
            lambda x: sentiment_map.get(str(x).lower(), 'Neutral')
        )

        # Count sentiments
        sentiments = ['Positive', 'Negative', 'Neutral']
        sentiment_counts = filtered_df['sentiment_normalized'].value_counts().to_dict()
        counts = [sentiment_counts.get(s, 0) for s in sentiments]

        if sum(counts) > 0:
            fig, ax = plt.subplots(figsize=(3, 3))
            wedges, texts, autotexts = ax.pie(
                counts, 
                labels=sentiments,
                autopct='%1.1f%%',
                startangle=90,
                colors=['#00cc99', '#ff66b3', 'gray'],
                textprops={'fontsize': 9}
            )
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.info("No sentiment data available for the current selection.")
    else:
        st.info("No sentiment data available for the current selection.")


# ---------------------------
# Entity visualization
# ---------------------------
st.subheader("🏷️ Top Named Entities")
if 'entities' in filtered_df.columns and not filtered_df['entities'].dropna().empty:
    all_entities = []
    for ents in filtered_df['entities'].dropna():
        all_entities.extend([e.strip() for e in ents.split(",") if e.strip()])

    if all_entities:
        entity_counts = Counter(all_entities).most_common(10)
        entity_df = pd.DataFrame(entity_counts, columns=["Entity", "Count"])
        st.bar_chart(entity_df.set_index("Entity"))
    else:
        st.info("No named entities detected in this selection.")
else:
    st.info("No entity data available.")

# ---------------------------
# Search results
# ---------------------------
st.subheader('🔎 Search Results')
if not filtered_df.empty:
    cols_to_show = ['title', 'url', 'category', 'sentiment']
    if 'publishedAt_IST' in filtered_df.columns:
        cols_to_show.insert(2, 'publishedAt_IST')
    if 'entities' in filtered_df.columns:
        cols_to_show.append('entities')

    st.dataframe(filtered_df[cols_to_show].reset_index(drop=True))
else:
    st.info("No search results to display.")
