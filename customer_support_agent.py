# (Agent logic: RAG + Order Lookup tool)

# customer_support_agent.py

import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader

def load_support_docs(docs_dir="docs"):
    all_docs = []
    for filename in os.listdir(docs_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(docs_dir, filename)
            loader = TextLoader(file_path)
            docs = loader.load()
            for d in docs:
                d.metadata["source"] = filename
            all_docs.extend(docs)
    return all_docs

def build_retriever(docs):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory="chroma_db")
    return vectordb.as_retriever()

def rag_tool_func(query, retriever):
    results = retriever.get_relevant_documents(query)
    if not results:
        return "Sorry, I couldn't find any information in our knowledge base."
    return "\n\n".join([f"From {r.metadata['source']}: {r.page_content.strip()}" for r in results])

def order_lookup_tool_func(order_id, orders):
    print("=====Printing order details New=====")
    print(order_id)
    order_id = order_id.replace("```","").strip()
    print(order_id)
    print(orders)
    for o in orders:
        print(o)
        print(order_id)
        print(o["order_id"] ,order_id )
        if o["order_id"] == order_id:
            print("Order found")
            return (f"Order ID: {o['order_id']}\n"
                    f"Item: {o['item']}\n"
                    f"Status: {o['status']}\n"
                    f"Date: {o['date']}")
    return f"Sorry, I could not find any order with ID {order_id}."

def create_agent(retriever, orders):
    rag_tool = Tool(
        name="KnowledgeBaseSearch",
        func=lambda query: rag_tool_func(query, retriever),
        description="Use this tool to answer customer support questions using company documents."
    )
    order_lookup_tool = Tool(
        name="OrderLookup",
        func=lambda order_id: order_lookup_tool_func(order_id, orders),
        description="Use this tool to look up the status of a customer's order by order ID. The user must provide an order ID."
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = initialize_agent(
        tools=[order_lookup_tool, rag_tool],
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=False,
        handle_parsing_errors=True
    )
    return agent
