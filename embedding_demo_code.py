# pip install openai scikit-learn numpy


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
load_dotenv()
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# Example code snippets
code1 = """def add(a, b): return a + b"""
code2 = """def multiply(a, b): return a * b"""
query = "generate a code for 2 number multiplication" # replace with multiplication

def get_embedding(text, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        model=model,
        input=text
    )
    return np.array(response.data[0].embedding)

# Get embeddings for each code snippet
code1_emb = get_embedding(code1).reshape(1, -1)
code2_emb = get_embedding(code2).reshape(1, -1)
query_emb = get_embedding(query).reshape(1, -1)

# Compute cosine similarities
print(f"Similarity between query and code1 {cosine_similarity(query_emb, code1_emb)[0][0]:.4f}")
print(f"Similarity between query and code2: {cosine_similarity(query_emb, code2_emb)[0][0]:.4f}")
