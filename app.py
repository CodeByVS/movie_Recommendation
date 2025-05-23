# Add this import if not already present
import pickle
import requests
from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
import pandas as pd
import os
import numpy as np

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load the movie data - add error handling for file loading
try:
    # Check if model files exist
    if os.path.exists('model/movie_list.pkl'):
        movies_df = pickle.load(open('model/movie_list.pkl', 'rb'))
    else:
        # If model files don't exist, create sample data
        from model.sample_data import create_sample_data
        create_sample_data()
        movies_df = pickle.load(open('model/movie_list.pkl', 'rb'))
        print("Created sample movie data for testing.")
except Exception as e:
    print(f"Error loading movie data: {e}")
    movies_df = pd.DataFrame(columns=['movie_id', 'title'])

# Load similarity matrix
try:
    if os.path.exists('model/similarity.pkl'):
        similarity = pickle.load(open('model/similarity.pkl', 'rb'))
    else:
        # Create dummy similarity matrix if needed
        num_movies = len(movies_df)
        similarity = np.identity(num_movies)  # Identity matrix as fallback
        print("Warning: Similarity matrix not found. Using identity matrix.")
except Exception as e:
    print(f"Error loading similarity data: {e}")
    similarity = np.array([])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route('/api/search')
def search():
    global movies_df
    query = request.args.get('query', '').lower()
    print(f"\n\n==== SEARCH API CALLED ====\nQuery: '{query}'")
    
    if not query:
        print("Empty query, returning empty results")
        return jsonify([])
    
    # Search in movie titles
    try:
        # Debug output for troubleshooting
        print(f"Movies dataframe shape: {movies_df.shape}")
        print(f"Movies dataframe columns: {movies_df.columns.tolist()}")
        
        # Check if the dataframe is empty
        if movies_df.empty:
            print("WARNING: Movies dataframe is empty!")
            # Try to reload the data
            if os.path.exists('model/movie_list.pkl'):
                movies_df = pickle.load(open('model/movie_list.pkl', 'rb'))
                print(f"Reloaded movies dataframe, new shape: {movies_df.shape}")
            else:
                print("Movie data file not found, creating sample data")
                from model.sample_data import create_sample_data
                create_sample_data()
                movies_df = pickle.load(open('model/movie_list.pkl', 'rb'))
                print(f"Created sample data, shape: {movies_df.shape}")
        
        # Improved search to handle partial matches better
        results = movies_df[movies_df['title'].str.lower().str.contains(query, na=False)]
        
        # Debug output
        print(f"Search query: '{query}', Found {len(results)} results")
        
        # Convert to list of dictionaries for JSON response
        search_results = []
        for _, movie in results.iterrows():
            # Get movie ID for image mapping
            movie_id = int(movie['movie_id'])
            
            # Use TMDB API style URL format for consistency
            # In a real app, this would be a real TMDB URL
            try:
                url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
                data = requests.get(url)
                if data.status_code == 200:
                    data = data.json()
                    poster_path = data.get('poster_path')
                    if poster_path:
                        # Use TMDB-style URL with the movie ID to create a consistent poster path
                        image_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                    else:
                        # Use a placeholder if no poster path is available
                        image_path = "https://via.placeholder.com/500x750?text=No+Poster+Available"
                else:
                    # Use a placeholder if the API request fails
                    image_path = "https://via.placeholder.com/500x750?text=No+Poster+Available"
            except Exception as e:
                print(f"Error fetching poster for movie ID {movie_id}: {e}")
                # Use a placeholder if there's an exception
                image_path = "https://via.placeholder.com/500x750?text=No+Poster+Available"
            
            # For a real application, you would use TMDB API to get poster paths
            # Example: poster_path = f'https://image.tmdb.org/t/p/w500/{movie["poster_path"]}'
            # But for this sample app, we'll use local images
            
            search_results.append({
                'movie_id': movie_id,
                'title': movie['title'],
                'poster_path': image_path
            })
        
        # If no results found with exact match, try more flexible matching
        if len(search_results) == 0:
            print("No exact matches found, trying flexible matching")
            # Try matching any word in the title
            for _, movie in movies_df.iterrows():
                title_lower = movie['title'].lower()
                if any(q in title_lower for q in query.split()):
                    search_results.append({
                        'movie_id': int(movie['movie_id']),
                        'title': movie['title']
                    })
            print(f"Flexible matching found {len(search_results)} results")
        
        # Return the results
        print(f"Returning {len(search_results[:10])} search results")
        print("==== SEARCH API COMPLETED ====\n")
        return jsonify(search_results[:10])  # Limit to 10 results
    except Exception as e:
        print(f"SEARCH ERROR: {e}")
        return jsonify({'error': 'An error occurred during search'}), 500

@app.route('/api/movies')
def get_movies():
    global movies_df
    try:
        # Return all movies
        all_movies = []
        for _, movie in movies_df.iterrows():
            all_movies.append({
                'movie_id': int(movie['movie_id']),
                'title': movie['title']
            })
        return jsonify(all_movies)
    except Exception as e:
        print(f"Error fetching all movies: {e}")
        return jsonify({'error': 'An error occurred while fetching movies'}), 500

@app.route('/api/recommend')
def recommend():
    global movies_df
    movie_name = request.args.get('movie', '')
    if not movie_name:
        return jsonify({'error': 'No movie provided'})
        
    print(f"\n\n==== RECOMMEND API CALLED ====\nMovie: '{movie_name}'")
    # Debug output for troubleshooting
    print(f"Movies dataframe shape: {movies_df.shape}")
    print(f"Movies dataframe columns: {movies_df.columns.tolist()}")
    
    try:
        # Find the movie index - using case-insensitive matching
        print(f"Searching for movie: '{movie_name}'")
        print(f"Available movies: {movies_df['title'].tolist()}")
        
        # First try exact match (case-insensitive)
        movie_matches = movies_df[movies_df['title'].str.lower() == movie_name.lower()]
        
        # If no exact match, try partial match
        if movie_matches.empty:
            print(f"No exact match found for '{movie_name}', trying partial matches")
            # Try to find movies that contain the search term
            movie_matches = movies_df[movies_df['title'].str.lower().str.contains(movie_name.lower(), na=False)]
        
        # If still no matches, try more flexible matching
        if movie_matches.empty:
            print(f"No partial matches found for '{movie_name}', trying word-by-word matching")
            # Try matching any word in the title
            for word in movie_name.lower().split():
                if len(word) > 2:  # Only consider words with more than 2 characters
                    word_matches = movies_df[movies_df['title'].str.lower().str.contains(word, na=False)]
                    if not word_matches.empty:
                        movie_matches = word_matches
                        print(f"Found matches using word: '{word}'")
                        break
        
        # If we found any matches, use the first one
        if movie_matches.empty:
            raise IndexError(f"No movie found matching '{movie_name}'")
            
        # Get the first match index
        idx = movie_matches.index[0]
        matched_title = movie_matches.iloc[0]['title']
        print(f"Found match: '{matched_title}' for query '{movie_name}'")
        
        # Get similar movies
        distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])        
        # Get top 5 recommendations
        recommendations = []
        
        # Debug output
        print(f"Found {len(distances)} similar movies for '{movie_name}'")
        
        # Make sure we have enough recommendations
        if len(distances) <= 1:
            print(f"Warning: Not enough similar movies found for '{movie_name}'")
            # Return empty recommendations with a message
            return jsonify({'error': 'Not enough similar movies found'})
        
        # Get top 5 recommendations (skip the first one as it's the movie itself)
        for i in distances[1:6]:
            # Check if index is valid before accessing
            if i[0] < len(movies_df):
                try:
                    movie_title = movies_df.iloc[i[0]]['title']
                    movie_id = int(movies_df.iloc[i[0]]['movie_id'])  # Convert int64 to Python int
                    similarity_score = float(i[1])
                
                    print(f"Recommending: '{movie_title}' with similarity {similarity_score:.2f}")
                    
                    try:
                        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
                        data = requests.get(url)
                        if data.status_code == 200:
                            data = data.json()
                            poster_path = data.get('poster_path')
                            if poster_path:
                                # Use TMDB-style URL with the movie ID to create a consistent poster path
                                image_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                            else:
                                # Use a placeholder if no poster path is available
                                image_path = "https://via.placeholder.com/500x750?text=No+Poster+Available"
                        else:
                            # Use a placeholder if the API request fails
                            image_path = "https://via.placeholder.com/500x750?text=No+Poster+Available"
                    except Exception as e:
                        print(f"Error fetching poster for recommendation movie ID {movie_id}: {e}")
                        # Use a placeholder if there's an exception
                        image_path = "https://via.placeholder.com/500x750?text=No+Poster+Available"
                    
                    recommendations.append({
                        'movie_id': movie_id,
                        'title': movie_title,
                        'similarity': similarity_score,
                        'poster_path': image_path
                    })
                except Exception as e:
                    print(f"Error processing recommendation at index {i[0]}: {e}")
                    # Continue to next recommendation
        
        print(f"Returning {len(recommendations)} recommendations")
        print("==== RECOMMEND API COMPLETED ====\n")
        return jsonify(recommendations)
    except (IndexError, KeyError) as e:
        print(f"Movie not found error: {e}")
        print(f"Searched for movie: '{movie_name}'")
        print(f"Available movies: {movies_df['title'].tolist()}")
        return jsonify({'error': f'Movie "{movie_name}" not found'}), 404
    except Exception as e:
        print(f"Recommendation error: {e}")
        print(f"Searched for movie: '{movie_name}'")
        print(f"Exception details: {str(e)}")
        return jsonify({'error': f'Sorry, we couldn\'t load recommendations for "{movie_name}". Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
