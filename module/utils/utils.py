from sentence_transformers import SentenceTransformer

def embed_text_huggingface(model, text):
    """
    Embed the given text using OPENAI's text-embedding-ada-002 model.

    Args:
        text (str): The text to be embedded.

    Returns:
        numpy.ndarray: The embedded text representation.
    """
    #Sentences are encoded by calling model.encode()
    embedding = model.encode(text)

    return embedding

import numpy as np
def vector_search(embeder, sentence, index, k):
    """
    Perform search retrival from FIASS

    Args:
        index: Import the index
        k: number of embedding to return

    Returns:

    """
    xq = np.array(embeder(sentence)).reshape(1,-1)
    D, I = index.search(xq, k)

    return D, I

def semantic_search_faiss(query_embedding, index, k):
    """
    Perform semantic search using FAISS and retrieve relevant documents based on the query.

    Args:
        query_embedding (numpy.ndarray): The embedding of the user's query.
        index_file (str): The file path to the saved FAISS index.
        k (int): The number of most similar documents to retrieve.

    Returns:
        List[int]: The indices of the most relevant documents.
    """

    print(query_embedding.shape)

    # Convert the query embedding to a numpy array
    query_np = np.array([query_embedding]).astype(np.float32)

    # Perform similarity search using FAISS
    D, indices = index.search(query_np, k)

    retrieved_indices = indices[0].tolist()

    return retrieved_indices

def _get_relevance_score(query_embedding, conversation_embedding):
    """
    Calculate the relevance score between the query embedding and a conversation embedding.
    Args:
        query_embedding (numpy.ndarray): The embedding of the query.
        conversation_embedding (numpy.ndarray): The embedding of the conversation.

    Returns:
        float: The relevance score between the embeddings.
    """

    # Calculate the cosine similarity between the embeddings
    similarity = np.dot(query_embedding, conversation_embedding) / (
        np.linalg.norm(query_embedding) * np.linalg.norm(conversation_embedding)
    )
    return similarity

import faiss
def write_embeddings_to_vector_store(embeddings, index_name):
    """
    Write the embeddings to a vector store using FAISS.

    Args:
        embeddings (numpy.ndarray): The array of embeddings.
        index_name (str): The name of the index.

    Returns:
        None
    """
    index = faiss.IndexFlatL2(embeddings.shape[1])  # Create a flat index with inner product (IP) similarity
    index.add(embeddings)  # type: ignore # Add the embeddings to the index
    faiss.write_index(index, index_name)  # Save the index to disk

    return index

# import openai
import time
def embed_text_openai(client, text, model="text-embedding-3-small"):
    """
    Embed the given text using OPENAI's text-embedding-3-small model.

    Args:
        text (str): The text to be embedded.

    Returns:
        numpy.ndarray: The embedded text representation.
    """
    text = text.replace("\n", " ")
    
    time.sleep(1)
    return client.embeddings.create(input = [text], model=model).data[0].embedding

import requests
import os
def embed_text_huggingfaceapi(texts, model_id = "sentence-transformers/all-MiniLM-L6-v2"):
    hf_token = os.environ['HF_TOKEN']
    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()