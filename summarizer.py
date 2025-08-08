import openai
import os

def summarize_reviews(reviews):
    openai.api_key  = os.getenv("OPENAI_API_KEY")
    prompt = f"Summarize these product reviews in 2-3 crisp bullet points :\n" + "\n".join(reviews)
    print("summarization prompt and reviews", prompt)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()
