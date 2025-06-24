import streamlit as st
import pandas as pd
import pickle
import requests
# import gdown
#
# file_id = '169h6rIaLkDWnNdMcjREHrCQzu6dkFbM6'
# url = f'https://drive.google.com/uc?id={file_id}'
# output = 'similarity.pkl'
# gdown.download(url, output, quiet=False)

# Fetch movie poster from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5d16a371a03e9332ce06f208e3b51cbe&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return "https://via.placeholder.com/300x450?text=No+Image"
    data = response.json()
    poster_path = data.get('poster_path', '')
    if not poster_path:
        return "https://via.placeholder.com/300x450?text=No+Image"
    return "https://image.tmdb.org/t/p/w500/" + poster_path


# Recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# Load data
movies_dict = pickle.load(open('Movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# UI
st.title("Movie Recommender System 🎬")

selected_movie = st.selectbox(
    "Select a movie you like:",
    movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])
