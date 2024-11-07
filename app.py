import streamlit as st
import pickle
import requests
import os


api_key = os.getenv("TMDB_API_KEY")

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title("Movie Recommender system")

selected_movie = st.selectbox(
    'Please select a movie from the list: ', 
    (movies_list)
)


def recommend(movie):
    movie_index =  movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    #Sorting similarity while retaning original indices
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:7]

    # Generate a list of recommended movie titles
    recommended_movies = []
    for i in movie_indices:
        movie_id = movies['movie_id'][i[0]]
        title = movies_list[i[0]]
        recommended_movies.append({movie_id: title})

    return recommended_movies

def fetch_poster(movie_id):
  
    url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, api_key)
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    st.subheader("Recommended movies:")

    # Display movies in rows of three
    for i in range(0, len(recommendations), 3):
        cols = st.columns(3)  # Creates 3 columns
        for j, movie in enumerate(recommendations[i:i+3]):
            movie_id = list(movie.keys())[0]
            title = list(movie.values())[0]
            
            with cols[j]:
                st.image(fetch_poster(movie_id))
                st.write(title)