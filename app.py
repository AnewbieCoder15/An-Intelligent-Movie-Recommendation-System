import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import string
import requests
import warnings
warnings.filterwarnings('ignore')
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']
def recommend(movie):
    movie_name = movie.lower().strip()
    movie_poster = []
    if movie_name not in list(movies_list['title']):
        for x in list(movies_list['title']):
            if x.find(movie_name) >= 0:
                index = movies_list[movies_list['title'] == x].index[0]
                similarities = similarity[index]
                indeces = sorted(list(enumerate(similarities)), reverse=True, key=lambda x: x[1])[0:10]
                list_of_movies = [ [movies_list['title'][x[0]],movies_list['id'][x[0]]] for x in indeces]
                movie_poster = [fetch_poster(x[1]) for x in list_of_movies]
                return list_of_movies , movie_poster
        vectorizer1 = CountVectorizer()
        cleaned_name = ''.join([char for char in movie_name if char not in string.punctuation])
        movielist = list(movies_df['modified_title'].apply(lambda x: ' '.join(x)))
        movielist.append(cleaned_name)
        df = pd.DataFrame({'movie_name': movielist})
        movie_title_vectorizer = vectorizer1.fit_transform(df['movie_name']).toarray()
        similar_names = cosine_similarity(movie_title_vectorizer)
        simi = similar_names[-1]
        indeces_1 = sorted(list(enumerate(simi)), reverse=True, key=lambda x: x[1])[0:10]
        list_of_movies_1 = [[movies_list['title'][x[0]],movies_list['id'][x[0]]] for x in indeces_1]
        movie_poster = [fetch_poster(x[1]) for x in list_of_movies_1]
        return list_of_movies_1, movie_poster
    index = movies_list[movies_list['title'] == movie_name].index[0]
    similarities = similarity[index]
    indeces = sorted(list(enumerate(similarities)), reverse=True, key=lambda x: x[1])[1:11]
    list_of_movies = [[movies_list['title'][x[0]],movies_list['id'][x[0]]] for x in indeces]
    movie_poster = [fetch_poster(x[1]) for x in list_of_movies]
    return list_of_movies, movie_poster
movies_list = pickle.load(open('movies_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies_df= pickle.load(open('movies.pkl','rb'))
st.title('Movie Recommender System')
st.write('You can either search a movie name or select a movie name from existing list')
movies = list(movies_list['title'].apply(lambda x: x.title()))
selected_movie_name_1 = st.text_input('Search Box :')
if st.button('Search'):
    recommended_movies, poster = recommend(selected_movie_name_1)
    cols = list(st.columns(5))
    for i in range(5):
        cols[i].text(recommended_movies[i][0].title())
        cols[i].image(poster[i], use_column_width=True)
    cols = list(st.columns(5))
    for i in range(5, 10):
        cols[i-5].text(recommended_movies[i][0].title())
        cols[i-5].image(poster[i], use_column_width=True)
selected_movie_name_2 = st.selectbox(
    'Welcome User!',
    movies
)
if st.button('Recommend'):
    recommended_movies, poster = recommend(selected_movie_name_2)
    cols = list(st.columns(5))
    for i in range(5):
        cols[i].text(recommended_movies[i][0].title())
        cols[i].image(poster[i], use_column_width=True)
    cols = list(st.columns(5))
    for i in range(5,10):
        cols[i-5].text(recommended_movies[i][0].title())
        cols[i-5].image(poster[i], use_column_width=True)
