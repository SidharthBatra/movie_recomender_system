import streamlit as st
import pickle 
import pandas as pd
import requests

# =======================
# Utility Functions
# =======================
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=174d4bf983cfa1999dc8457fb84e8cd3'
    )
    data = response.json()
    return 'https://image.tmdb.org/t/p/original' + data['poster_path']

def fetch_rating(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=174d4bf983cfa1999dc8457fb84e8cd3'
    )
    data = response.json()
    return data['vote_average']

# =======================
# Load Data
# =======================
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# import pickle
import gzip

# Compress your similarity.pkl
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

with gzip.open("similarity_compressed.pkl.gz", "wb") as f:
    pickle.dump(similarity, f)

# similarity = pickle.load(open('similarity.pkl', 'rb'))

# =======================
# Streamlit UI
# =======================
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
st.title("🎬 Movie Recommender System")
st.markdown(
    "<p style='font-size:18px;'>Discover your next favorite movie with our smart recommendation system! 🍿</p>",
    unsafe_allow_html=True
)

# =======================
# Recommendation Function
# =======================
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies, posters, ratings = [], [], []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
        ratings.append(fetch_rating(movie_id))
    return recommended_movies, posters, ratings

# =======================
# User Input
# =======================
option = st.selectbox("🎥 Choose your favorite movie", movies['title'].values)

if st.button("🔍 Show Recommendations"):
    names, posters, ratings = recommend(option)

    st.markdown("---")
    st.subheader("✨ Recommended Movies for You")

    cols = st.columns(5, gap="medium")
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.markdown(f"<h4 style='text-align:center;'>{names[idx]}</h4>", unsafe_allow_html=True)

            # Convert rating to stars
            stars = "⭐" * int(ratings[idx] // 2)  # TMDB ratings are out of 10, so divide by 2
            st.markdown(f"<p style='text-align:center;'>{stars} ({ratings[idx]:.1f}/10)</p>", unsafe_allow_html=True)

