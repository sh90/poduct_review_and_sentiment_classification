import openai
import os

api_key = os.getenv("OPENAI_API_KEY")
def summarize_reviews(reviews):
    openai.api_key = api_key
    prompt = f"Summarize these product reviews in 2-3 sentences:\n" + "\n".join(reviews)
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()
