# pip install openai scikit-learn
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
load_dotenv()
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

sentence1 = "we allow 7 day return policy"
sentence2 = "we can't process refund for electronics item"
query = "tell me about your return policy"

# "text-embedding-ada-002"
def get_embedding(text, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        model=model,
        input=text
    )
    # The embedding is in response.data[0].embedding
    return np.array(response.data[0].embedding)

sentence1_emb = get_embedding(sentence1).reshape(1, -1)
sentence2_emb = get_embedding(sentence2).reshape(1, -1)
query_emb = get_embedding(query).reshape(1, -1)

print(cosine_similarity(query_emb, sentence1_emb))
print(cosine_similarity(query_emb, sentence2_emb))
