import openai

import os

api_key = os.getenv("OPENAI_API_KEY")

def analyze_sentiment(reviews):
    openai.api_key = api_key
    prompt = "Classify the overall sentiment of these product reviews as 'positive', 'neutral', or 'negative'. Just give one word answer along with relevant emoji icon.\n" + "\n".join(reviews)
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,
        temperature=0
    )
    return response.choices[0].message.content.strip().lower()

def analyze_sentiments_per_review(reviews):
    openai.api_key = api_key
    out = []
    for review in reviews:
        prompt = f"Classify the sentiment of this product review as 'positive', 'neutral', or 'negative'. Just give one word answer along with relevant emoji icon.\n{review}"
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0
        )
        out.append(response.choices[0].message.content.strip().lower())
    return out
