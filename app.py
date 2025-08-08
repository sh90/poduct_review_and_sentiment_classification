
import os
from dotenv import load_dotenv

from amazon_reviews import fetch_amazon_reviews
from summarizer import summarize_reviews
from sentiment import analyze_sentiment, analyze_sentiments_per_review
from wordcloud_gen import plot_wordcloud
import streamlit as st
from utils import load_reviews_from_csv
from utils import load_reviews_from_db, get_unique_products

load_dotenv()
# ----- Step 1: Review Source -----
# ----- Step 1: Source Selection -----
st.header("Step 1: Choose Source for Product Reviews")
source = st.radio(
    "Select input source",
    ("Paste / Upload CSV", "Database Table", "Amazon Product URL"),
    key="review_source"
)

# ---- Step 1a: Data Source Logic ----
reviews = []

if source == "Paste / Upload CSV":
    upload = st.file_uploader("Upload CSV file of reviews", type=["csv"], key="csv_uploader")
    if upload:
        loaded = load_reviews_from_csv(upload)
        st.session_state['csv_reviews'] = loaded
        st.success(f"Loaded {len(loaded)} reviews from CSV.")
    else:
        default = """Great phone! Battery lasts forever.
Camera quality is decent, but not the best.
Really disappointed, phone started lagging after a week.
Absolutely love it, fast performance and clean display!
Mediocre speaker quality, but overall good value."""
        reviews_text = st.text_area(
            "Or, paste product reviews (one per line):", value=default, height=200, key="csv_textarea"
        )
        loaded = [r.strip() for r in reviews_text.strip().split("\n") if r.strip()]
        st.session_state['csv_reviews'] = loaded
    reviews = st.session_state.get('csv_reviews', [])

elif source == "Database Table":
    table = st.text_input("Enter table name (default: product_reviews)", value="product_reviews", key="db_table")
    products = []
    if table:
        try:
            products = get_unique_products(table)
        except Exception as e:
            st.error(f"Could not load products: {e}")
    product = st.selectbox(
        "(Optional) Select product name to filter", ["All"] + products, index=0 if products else 0, key="db_product"
    )
    if st.button("Load from DB", key="db_load"):
        loaded = load_reviews_from_db(
            table,
            product_name=None if product == "All" else product
        )
        st.session_state['db_reviews'] = loaded
        st.success(f"Loaded {len(loaded)} reviews from database.")
    reviews = st.session_state.get('db_reviews', [])

elif source == "Amazon Product URL":
    amazon_url = st.text_input("Paste Amazon product URL:", key="amazon_url")
    serpapi_key = st.text_input("Enter Search Api Key:", type="password", key="serpapi_key")
    if st.button("Fetch Amazon Reviews", key="amazon_fetch"):
        with st.spinner("Fetching reviews from Amazon..."):
            loaded, err = fetch_amazon_reviews(amazon_url, serpapi_key)
        if err:
            st.error(f"Failed: {err}")
        elif loaded:
            st.session_state['amazon_reviews'] = loaded
            st.success(f"Fetched {len(loaded)} reviews from Amazon!")
        else:
            st.warning("No reviews found. Check URL or try another product.")
    reviews = st.session_state.get('amazon_reviews', [])

# ----- Step 2: Analysis Pipeline -----
if reviews and st.button("Analyze Reviews", key="analyze_btn"):
    # Summarize
    st.header("Step 2: Summarize Reviews")
    summary = summarize_reviews(reviews )
    st.write(summary)

    # Word Cloud
    st.header("Step 3: Word Cloud")
    plot_wordcloud(reviews)

    # Sentiment analysis (overall)
    st.header("Step 4: Sentiment Analysis")
    overall_sentiment = analyze_sentiment(reviews )
    st.write(f"**Overall Sentiment:** {overall_sentiment.capitalize()}")

    # emoji_url = generate_emoji_image(overall_sentiment )
    # st.image(emoji_url, caption=f"Overall Sentiment Emoji: {overall_sentiment.capitalize()}", width=128)

    # Sentiment analysis per review + image per review
    st.header("Step 5: Sentiment & Emoji per Review")
    sentiments = analyze_sentiments_per_review(reviews)
    for i, (rev, sent) in enumerate(zip(reviews, sentiments )):
        st.markdown(f"**Review {i+1}:** {rev}")
        st.write(f"Sentiment: {sent.capitalize()}")
