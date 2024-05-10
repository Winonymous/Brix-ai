import pandas as pd
import numpy as np
from function import embed_text_huggingface, write_embeddings_to_vector_store, embed_text_openai, embed_text_huggingfaceapi
from sentence_transformers import SentenceTransformer
from openai import OpenAI

class vector():
    def __init__(self, name, df_file) -> None:
        # self.model = SentenceTransformer(name)
        # self.client = OpenAI()
        # Read the dataset
        self.dataset = pd.read_csv(df_file)
        # Remove all null value
        self.dataset.dropna(inplace = True)
    
    def create_vector_store(self, column, store_file):
        # Convert to embeddings
        # embeddings = self.dataset[column].apply(lambda x: embed_text_huggingface(self.model, x))
        # embeddings = self.dataset[column].apply(lambda x: embed_text_huggingfaceapi(self.client, x))
        embeddings = self.dataset[column].apply(lambda x: embed_text_huggingfaceapi(x))


        original_embeddings = np.vstack(embeddings.values)

        self.index = write_embeddings_to_vector_store(original_embeddings, store_file)

        return self.index
    
def main():
    print("Loading Model")
    create_vector = vector('paraphrase-MiniLM-L6-v2', "Resource/Brix guest query and response.csv")
    print("Creating Vector Store")
    create_vector.create_vector_store("Questions", "Resource/openai.index")    


if __name__ == '__main__':
	main()