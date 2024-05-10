import faiss
from .function import embed_text_huggingface, semantic_search_faiss, _get_relevance_score, embed_text_huggingfaceapi
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

class FindMatch():
    def __init__(self, index_file, model_name, df_file) -> None:
        self.index_file = index_file  # Choose a file path to save the FAISS index
        # self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(index_file)
        self.df = pd.read_csv(df_file)
        self.df.dropna(inplace = True)

    
    def find_match(self, query_text, k, threshold = 0.7):
        query_embedding = np.array(embed_text_huggingfaceapi(query_text))

        k = 3  # Retrieve top-k most similar documents
        retrieved_indices = semantic_search_faiss(query_embedding, self.index, k)

        # try: 
        # Ensure retrieved_indices are within the valid range
        retrieved_indices = [idx for idx in retrieved_indices if idx < len(self.df)]

        # Retrieve the corresponding conversations
        relevant_conversations = self.df.iloc[retrieved_indices]

        retrieved = relevant_conversations[relevant_conversations['Questions'].apply(
            lambda x: _get_relevance_score(embed_text_huggingfaceapi(x), 
                                        query_embedding)) > threshold]
        
        resp = retrieved['Answers'].values 
        if len(resp) > 0:
            return resp[0]
        else:
             return "I don't know"
        # except:
        #     return ["I don't know"]
    
def main():
    print("Loading Matcher")
    matcher = FindMatch("Resource/openai.index", 'paraphrase-MiniLM-L6-v2', "Resource/Brix guest query and response.csv")
    print("Find Match")
    resp = matcher.find_match("Where is Bells University", 1)
    print(resp)
    

if __name__ == '__main__':
	main()