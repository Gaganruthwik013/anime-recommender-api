from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os

app = Flask(__name__)

# Load dataset
data = pd.read_csv('anime.csv')
data = data.dropna(subset=['genre'])

# Recommendation function
def get_recommendations(genre, n=10):
    # Filter for matching genre
    matches = data[data['genre'].str.contains(genre, case=False, na=False)]
    if matches.empty:
        return []

    # Use only a small subset to reduce memory
    subset = data.copy()

    # TF-IDF and Cosine Similarity only for this request
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(subset['genre'])

    idx = matches.index[0]
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n+1]
    anime_indices = [i[0] for i in sim_scores]
    return subset.iloc[anime_indices][['name', 'rating']].to_dict(orient='records')

# Home route
@app.route('/')
def home():
    return '✅ Anime Recommendation API is running! Use /recommend?genre=action'

# Recommendation route
@app.route('/recommend', methods=['GET'])
def recommend():
    genre = request.args.get('genre')
    if not genre:
        return jsonify({'error': 'Genre parameter is required'}), 400
    results = get_recommendations(genre)
    return jsonify(results)

# Render-specific fix for port binding
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render sets this automatically
    app.run(host='0.0.0.0', port=port)
