This repository hosts a content-based Movie Recommendation System that analyzes film attributes—genres, keywords, cast, crew, and plot—to suggest similar titles using TF-IDF vectorization and cosine similarity. It provides a Flask-powered backend with RESTful API endpoints and a responsive frontend for interactive recommendations.


About
The Movie Recommendation System processes a dataset of ~5,000 films from TMDB to compute similarity scores based on combined textual features. It leverages TF-IDF to represent each movie as a high-dimensional vector and computes cosine similarity to identify the most related titles for any given film.

Features
Content-based filtering with TF-IDF and cosine similarity

RESTful API endpoints for searching and recommending movies

Responsive web interface displaying movie posters and titles

Preprocessing pipeline with data cleaning, feature extraction, and model serialization

Visualizations of genre distributions, similarity heatmaps, and recommendation examples

Built With
Backend: Python, Flask, NumPy, Pandas, scikit-learn

Data Processing: TF-IDF Vectorization, Cosine Similarity

Frontend: HTML, CSS, JavaScript

Visualization: Matplotlib, Seaborn

Storage: Pickle for model and similarity matrix serialization

Prerequisites
Python 3.7+

pip 

TMDB 5000 Movie Dataset (downloadable from Kaggle if not present locally)
