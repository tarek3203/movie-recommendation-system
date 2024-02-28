import streamlit as st
import pickle
import pandas as pd
import requests
import sklearn


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_title = movies['title'].values

def fetch_posters(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=66c5761ccdce111133e62fe2cc067a12&language=en-US'.format(movie_id))

    response_json = response.json()

    # st.text(response_json)
    # st.text('https://api.themoviedb.org/3/movie/{}?api_key=66c5761ccdce111133e62fe2cc067a12&language=en-US'.format(movie_id))

    return "https://image.tmdb.org/t/p/w500/" + response_json['poster_path']

def recommend_movies(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1: 6]
    recommend = []
    recommend_movies_poster = []
    for i in movies_list:
        movies_id = movies.iloc[i[0]].movie_id

        recommend.append(movies.iloc[i[0]].title)

        # fetch posters from API
        recommend_movies_poster.append(fetch_posters(movies_id))



    return recommend, recommend_movies_poster

st.title('movie-recommended-system')


selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies_title)


if st.button('Recommended Movies'):
    names, posters = recommend_movies(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])
