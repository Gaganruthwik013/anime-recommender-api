from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

# Load dataset
data = pd.read_csv('anime.csv')
data = data.dropna(subset=['genre'])

# TF-IDF vectorization on genre
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['genre'])

# Cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Recommendation function
def get_recommendations(genre, n=10):
    matches = data[data['genre'].str.contains(genre, case=False, na=False)]
    if matches.empty:
        return []
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
    app.run(debug=True)

