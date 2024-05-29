# import os
import chromadb

import pandas as pd

from langchain_community.embeddings import HuggingFaceHubEmbeddings

from chromadb.api.types import Documents

from .utils.langchainutils import LangChainEmbeddingAdapter
    

class ClassRetreival():
    def __init__(self, client, embeddings = HuggingFaceHubEmbeddings()) -> None:
        self.collection = client.get_collection(name="Retrievaldb", embedding_function = LangChainEmbeddingAdapter(embeddings))
    
    def get_response(self, query_text):
        results = self.collection.query(
                query_texts=[query_text], # Chroma will embed this for you
                n_results=1 # how many results to return
            )
        
        # print(results)
        
        return results['metadatas'][0][0]['Answers'], results['distances'][0][0]


def main():
    df_file = "Resource/Brix guest query and response.csv"

    # Chroma Client
    chroma_client = chromadb.HttpClient(host='localhost', port=8000)
    
    RetrivalModel = ClassRetreival(chroma_client, embeddings = HuggingFaceHubEmbeddings())
    
    print(RetrivalModel.get_response("What is the Location of Bells University"))
    
    return 

if __name__ == '__main__':
	main()