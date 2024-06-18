import streamlit as st
import time


youtube_link = st.text_input("Youtube Playlist Link",placeholder="https://www.youtube.com/watch?playlist")
st.divider()
st.write("The current movie title is", youtube_link)


if st.sidebar.button("reset"):
    st.experimental_rerun()