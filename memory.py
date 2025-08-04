# RAG based implementation
import glob
import chromadb
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
open_ai_key = os.getenv("OPENAI_API_KEY")

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("codebase")

def get_code_files(root_dir, exts=('.py',)):
    code_files = []
    for ext in exts:
        code_files += glob.glob(f"{root_dir}/**/*{ext}", recursive=True)
    return code_files

def chunk_code_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    chunks = []
    chunk, count = "", 0
    for line in lines:
        chunk += line
        count += 1
        if count >= 20 or line.strip() == "":
            if chunk.strip():
                chunks.append(chunk.strip())
            chunk, count = "", 0
    if chunk.strip():
        chunks.append(chunk.strip())
    return chunks

def ingest_codebase(root_dir):
    files = get_code_files(root_dir)
    docs, ids = [], []
    for file in files:
        chunks = chunk_code_file(file)
        for i, chunk in enumerate(chunks):
            docs.append(chunk)
            ids.append(f"{os.path.basename(file)}_{i}")
    embeddings = OpenAIEmbeddings(openai_api_key=open_ai_key).embed_documents(docs)
    collection.add(documents=docs, ids=ids, embeddings=embeddings)
    print(f"Ingested {len(docs)} code chunks from {len(files)} files.")

def retrieve_relevant_chunks(query, k=4):
    embedding = OpenAIEmbeddings(openai_api_key=open_ai_key).embed_query(query)
    results = collection.query(query_embeddings=[embedding], n_results=k)
    return list(zip(results['documents'][0], results['ids'][0]))
