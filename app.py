from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load dataset at app start
data = pd.read_csv('anime.csv')
data = data.dropna(subset=['genre'])

# TF-IDF vectorizer (to be used for each request)
tfidf = TfidfVectorizer(stop_words='english')

# Function to get recommendations based on genre
def get_recommendations(genre, n=10):
    logging.debug(f"Getting recommendations for genre: {genre}")
    
    # Filter for matching genre
    matches = data[data['genre'].str.contains(genre, case=False, na=False)]
    if matches.empty:
        return []

    # TF-IDF and Cosine Similarity for this request
    tfidf_matrix = tfidf.fit_transform(data['genre'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    idx = matches.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n+1]
    anime_indices = [i[0] for i in sim_scores]
    
    return data.iloc[anime_indices][['name', 'rating']].to_dict(orient='records')

# API route
@app.route('/recommend', methods=['GET'])
def recommend():
    genre = request.args.get('genre')
    if not genre:
        return jsonify({'error': 'Genre parameter is required'}), 400
    results = get_recommendations(genre)
    return jsonify(results)

if __name__ == '__main__':
    # Run the app on all available IP addresses, port 5000
    app.run(host='0.0.0.0', port=5000)
