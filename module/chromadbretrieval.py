# import os
import chromadb

import pandas as pd

from langchain_community.embeddings import HuggingFaceHubEmbeddings

# from langchain_chroma import Chroma

from langchain_core.embeddings import Embeddings
from chromadb.api.types import EmbeddingFunction, Documents


class LangChainEmbeddingAdapter(EmbeddingFunction[Documents]):
    def __init__(self, ef: Embeddings):
        self.ef = ef

    def __call__(self, input: Documents) -> Embeddings:
        return self.ef.embed_documents(input)
    

class ClassRetreival():
    def __init__(self, client, df_file = None, embeddings = HuggingFaceHubEmbeddings()) -> None:
        self.collection = client.get_or_create_collection(name="Retrievaldf", embedding_function = LangChainEmbeddingAdapter(embeddings))
        if df_file:
            df = pd.read_csv(df_file)
            df.dropna(inplace=True)

            self.collection.add(
                documents=list(df['Questions']),
                ids=list(df['S/N'].astype(str)),
                metadatas = df.drop(['Questions'], axis = 1).to_dict('records')
            )

    
    def get_response(self, query_text):
        results = self.collection.query(
                query_texts=[query_text], # Chroma will embed this for you
                n_results=1 # how many results to return
            )
        
        return results['metadatas'][0][0]['Answers'], results['distances'][0][0]


def main():
    df_file = "Resource/Brix guest query and response.csv"

    # Chroma Client
    chroma_client = chromadb.PersistentClient(path="Resource/chroma_db")
    
    RetrivalModel = ClassRetreival(chroma_client, embeddings = HuggingFaceHubEmbeddings())
    print(RetrivalModel.get_response("What is the Location of Bells University"))

if __name__ == '__main__':
	main()