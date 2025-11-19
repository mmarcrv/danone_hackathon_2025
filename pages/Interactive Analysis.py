import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import hdbscan
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import nltk
from nltk.corpus import wordnet

nltk.download('stopwords')
nltk.download('wordnet')

# ==========================================
# 2. STOPWORDS AVANZADAS
# ==========================================
from nltk.corpus import stopwords

# --- Streamlit CSV uploader: replace `file_path` usage with uploaded file ---
uploaded_file = None
try:
    # If running as a Streamlit page, show uploader
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
except Exception:
    # Not running in Streamlit context (e.g., script mode); fall back to file_path if defined
    uploaded_file = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # If file_path variable exists (legacy), prefer it; otherwise stop when running in Streamlit
    if 'file_path' in globals() and file_path:
        df = pd.read_csv(file_path)
    else:
        # If inside Streamlit, inform user and stop execution of the page
        if 'st' in globals():
            st.info("Please upload a CSV file to run the analysis (use the uploader above).")
            st.stop()
        else:
            raise ValueError("No CSV file provided: set `file_path` or run inside Streamlit and upload a CSV.")
stopwords_enhanced = set(stopwords.words('english'))
# añadir preposiciones, pronombres y auxiliares
custom_stopwords = ['he','she','it','they','we','i','you','me','my','mine','us','our','ours',
                    'in','on','at','by','with','for','to','from','of','as','has','have','do','does','did','is','are','was','were','be']
stopwords_enhanced.update(custom_stopwords)

# ==========================================
# 3. EMBEDDINGS
# ==========================================
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
embeddings = model.encode(df["full_text"].tolist(), show_progress_bar=True)

# ==========================================
# 4. CLUSTERING HDBSCAN
# ==========================================
clusterer = hdbscan.HDBSCAN(min_cluster_size=20, min_samples=10, metric='euclidean')
df["cluster"] = clusterer.fit_predict(embeddings)
print("\n=== Cluster counts ===")
print(df["cluster"].value_counts())

# ==========================================
# 5. MANUAL TOPICS (keywords + sinónimos)
# ==========================================
# Función para ampliar palabras clave con sinónimos de WordNet
def expand_keywords(keywords):
    expanded = set(keywords)
    for word in keywords:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded.add(lemma.name().replace('_',' ').lower())
    return list(expanded)

topic_keywords = {
    "flavour": expand_keywords(["flavour", "taste", "sweet", "bitter", "aroma", "delicious"]),
    "texture": expand_keywords(["creamy", "thick", "liquid", "grainy", "texture", "smooth"]),
    "packaging": expand_keywords(["package", "bottle", "box", "cap", "broken", "expiry", "label"]),
    "health": expand_keywords(["diabetes", "cholesterol", "healthy", "sugar-free", "benefit", "0%"]),
    "price": expand_keywords(["expensive", "price", "cheap", "cost", "value"]),
    "quality": expand_keywords(["good", "bad", "fresh", "smell", "defective", "stale"])
}

# ==========================================
# 6. MULTI-TOPIC ASSIGNMENT
# ==========================================
def assign_topics_multi(text, topic_keywords):
    assigned = []
    text_lower = text.lower()
    for topic, words in topic_keywords.items():
        for w in words:
            if w in text_lower:
                assigned.append(topic)
                break
    return assigned if assigned else ["other"]

df["topics"] = df["full_text"].apply(lambda x: assign_topics_multi(x, topic_keywords))

# ==========================================
# 7. SENTIMENT
# ==========================================
def get_sentiment(x):
    if x >= 4: return "positive"
    if x <= 2: return "negative"
    return "neutral"

df["sentiment"] = df["rating"].apply(get_sentiment)

# ==========================================
# 8. DETECCION DE KEYWORDS DE CLUSTERS "OTHER"
# ==========================================
vectorizer_count = CountVectorizer(stop_words=stopwords_enhanced, max_features=2000, ngram_range=(1,2))
X_count = vectorizer_count.fit_transform(df["full_text"])

cluster_keywords = {}
for cl in df["cluster"].unique():
    idx = df[df["cluster"]==cl].index
    if len(idx) < 5: 
        continue
    subset = X_count[idx]
    sums = subset.sum(axis=0)
    words_freq = [(word, sums[0,i]) for word,i in vectorizer_count.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: -x[1])
    cluster_keywords[cl] = words_freq[:15]

# Mostrar keywords de clusters
for cl, wf in cluster_keywords.items():
    print(f"\nCluster {cl} top keywords:")
    for w,f in wf:
        print(f"{w} ({f})")

# ==========================================
# 9. KPIs MULTI-TOPIC
# ==========================================
all_topics_flat = [t for sublist in df["topics"] for t in sublist]
topic_volume = Counter(all_topics_flat)
print("\n=== TOPIC VOLUME (multi-topic) ===")
print(topic_volume)

# Sentiment per topic
sentiment_topic = {}
for topic in topic_keywords.keys():
    sentiment_counts = df[df["topics"].apply(lambda x: topic in x)].groupby("sentiment").size()
    sentiment_topic[topic] = sentiment_counts
sentiment_topic_df = pd.DataFrame(sentiment_topic).fillna(0).astype(int)
print("\n=== SENTIMENT PER TOPIC ===")
print(sentiment_topic_df)

# ==========================================
# 10. VISUALIZACIONES
# ==========================================
plt.figure(figsize=(12,5))
sns.barplot(x=list(topic_volume.keys()), y=list(topic_volume.values()), palette="viridis")
plt.title("Number of Reviews per Topic (multi-topic)")
plt.xticks(rotation=45)
plt.show()

sentiment_topic_df.plot(kind="bar", stacked=True, figsize=(12,5))
plt.title("Sentiment per Topic (multi-topic)")
plt.xticks(rotation=45)
plt.show()

# Top keywords por cluster (gráficos)
for cl, wf in cluster_keywords.items():
    words = [w for w,_ in wf]
    freqs = [f for _,f in wf]
    plt.figure(figsize=(8,4))
    sns.barplot(x=freqs, y=words, palette="viridis")
    plt.title(f"Top Keywords - Cluster {cl}")
    plt.xlabel("Frequency")
    plt.ylabel("Keyword")
    plt.show()



import requests
import json

url = "https://routellm.abacus.ai/v1/chat/completions"
headers = {"Authorization": "Bearer s2_9eb1acc8c0914ca2817c26df7a1e2b10", "Content-Type": "application/json"}
stream = False
payload = {
  "model": "gpt-5",
  "messages": [
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ],
  "stream": stream
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json())