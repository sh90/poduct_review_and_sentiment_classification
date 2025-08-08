from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

def plot_wordcloud(reviews):
    text = " ".join(reviews)
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
