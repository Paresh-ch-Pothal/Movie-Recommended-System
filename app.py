import streamlit as st
import pickle
import pandas as pd
import requests
import bz2

def fetch_poster(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=c425ca4e91dd52dd7b567e4e4be16e3a&language=en-US".format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/original"+data["poster_path"]

with bz2.BZ2File("similarity.pbz2", "rb") as f:
    similarity = pickle.load(f)

def recommend(movie):
    li=[]
    recommend_movies_poster=[]
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        li.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
    return li,recommend_movies_poster

movies_dict=pickle.load(open("movie_dict.pkl","rb"))
movies=pd.DataFrame(movies_dict)
st.title("Movie Recommended System")
selected_movie_name=st.selectbox("Type Your Movie Name",options=movies["title"].values)

if st.button("Recommend"):
    names,poster=recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        col1.image(poster[0],width=150)
        col1.write(names[0])
    with col2:
        col2.image(poster[1],width=150)
        col2.write(names[1])
    with col3:
        col3.image(poster[2],width=150)
        col3.write(names[2])
    with col4:
        col4.image(poster[3],width=150)
        col4.write(names[3])
    with col5:
        col5.image(poster[4],width=150)
        col5.write(names[4])