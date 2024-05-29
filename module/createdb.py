import chromadb
from utils.langchainutils import LangChainEmbeddingAdapter
from langchain_community.embeddings import HuggingFaceHubEmbeddings

import pandas as pd

def createretrivealdb(client, df_file, embeddings = HuggingFaceHubEmbeddings()):
    collection = client.get_or_create_collection(name="Retrievaldb", embedding_function = LangChainEmbeddingAdapter(embeddings))

    if df_file:
        df = pd.read_csv(df_file)
        df.dropna(inplace=True)

        # Find the files
        files = collection.get(
            ids=list(df['S/N'].astype(str))
            # where={"style": "style1"}ids=["id1", "id2", "id3", ...],
        )

        not_added = [index for index in df['S/N'] if str(index) not in files['ids']]
        
        print(not_added)

        not_added_df = df[df['S/N'].apply(lambda x: x in not_added)]

        print(not_added_df)

        if len(not_added_df > 0):
            collection.add(
                documents=list(not_added_df['Questions']),
                ids=list(not_added_df['S/N'].astype(str)),
                metadatas = not_added_df.drop(['Questions'], axis = 1).to_dict('records')
            )

def main():
    chroma_client = chromadb.PersistentClient(path="Resource/chroma_db2")
    df_file = "Resource/Brix guest query and response.csv"

    createretrivealdb(chroma_client, df_file, embeddings = HuggingFaceHubEmbeddings())

if __name__ == '__main__':
	main()