import streamlit as st 
import pickle
import pandas as pd 
import requests
import gzip
import os

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=9e93085db9bcf8f9866f933a1780b13f&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key= lambda x: x[1])[1:6]
    
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API 
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# movies_dict = pickle.load(open('movie_dict.pkl','rb'))
model_file_path = "movie_dict.pkl.gz"
try:
    with gzip.open(model_file_path, "rb") as f:
        movie_dict = pickle.load(f)
except FileNotFoundError:
    st.error("Model file not found.")
except Exception as e:
    st.error(f"Error occurred: {e}")
movies  = pd.DataFrame(movie_dict)

# similarity = pickle.load(open('similarity.pkl','rb'))
model_file_path = "similarity.pkl.gz"
try:
    with gzip.open(model_file_path, "rb") as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    st.error("Model file not found.")
except Exception as e:
    st.error(f"Error occurred: {e}")

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('How would you like to be contacted?', movies['title'].values)

if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])