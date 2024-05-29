from .utils.langchainutils import extract_pdf, load_prompt

import os
import pandas as pd

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
# from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_huggingface.llms import HuggingFaceEndpoint
from langchain.chains.question_answering import load_qa_chain


class HandBookChat():
    def __init__(self, pdf_file, llm_id = None, llm = None, embeddings = None, 
                 prompt_path = "module/prompts/basicqa.txt", map_prompt_path = "module/prompts/question_prompt_template.txt", 
                 combine_prompt_path = "module/prompts/combine_prompt_template.txt", refine_prompt_path = "module/prompts/refine_prompt_template.txt", 
                 initial_question_prompt_path = "module/prompts/initial_question_prompt_template.txt", response_refine_path = "module/prompts/refine_response.txt",
                 response_refine_personalized_path = "module/prompts/refine_personalized_response.txt") -> None:
        ## Define function for pdf
        self.pdf_file = pdf_file
        self.pages = extract_pdf(pdf_file)

        ## Define for llm
        if llm_id:
            self.llm_id = llm_id
            self.llm = HuggingFaceEndpoint(
                repo_id= self.llm_id, temperature=0.5, huggingfacehub_api_token=os.environ['HF_TOKEN']
                ) # type: ignore
            self.embeddings = HuggingFaceHubEmbeddings() # type: ignore
        elif llm:
            self.llm = llm
        elif embeddings:
            self.embeddings = embeddings
        
        if not self.llm:
            raise TypeError
        if not self.embeddings:
            raise TypeError
        

        ## Basic Prompt
        prompt_template = load_prompt(prompt_path)
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        self.basicqa = load_qa_chain(self.llm, chain_type="stuff", prompt=prompt)
        
        ## Map Reduce 
        question_prompt_template = load_prompt(map_prompt_path)
        
        question_prompt = PromptTemplate(
            template=question_prompt_template, input_variables=["context", "question"]
        )

        combine_prompt_template = load_prompt(combine_prompt_path)
        combine_prompt = PromptTemplate(
            template=combine_prompt_template, input_variables=["summaries", "question"]
        )

        self.map_reduce_chain = load_qa_chain(
            self.llm,
            chain_type="map_reduce",
            return_intermediate_steps=True,
            question_prompt=question_prompt,
            combine_prompt=combine_prompt,
        )

        ## Refine 
        refine_prompt_template = load_prompt(refine_prompt_path)
        refine_prompt = PromptTemplate(
            input_variables=["question", "existing_answer", "context_str"],
            template=refine_prompt_template,
        )


        initial_question_prompt_template = load_prompt(initial_question_prompt_path)

        initial_question_prompt = PromptTemplate(
            input_variables=["context_str", "question"],
            template=initial_question_prompt_template,
        )

        self.refine_chain = load_qa_chain(
            self.llm,
            chain_type="refine",
            return_intermediate_steps=True,
            question_prompt=initial_question_prompt,
            refine_prompt=refine_prompt,
        )

        ## Refine response Guest
        response_refine_prompt = load_prompt(response_refine_path)
        prompt = PromptTemplate(
            template=response_refine_prompt, input_variables=["question", "answer"]
        )

        self.refine_llm_chain = LLMChain(
            prompt=prompt,
            llm=self.llm
        )
        
        ## Refine response Personalized
        response_refine_personalized_prompt = load_prompt(response_refine_personalized_path)
        personalized_prompt = PromptTemplate(
            template=response_refine_personalized_prompt, input_variables=["question", "answer", "name", "department"]
        )

        self.refine_llm_pesornalizaed_chain = LLMChain(
            prompt=personalized_prompt,
            llm=self.llm
        )
        

    def respond(self, question, page_start = 0, page_stop = 2, type = 'mapreduce'):

        if not page_start:
            pages = self.pages[:page_stop]
        elif not page_stop:
            pages = self.pages[page_start:]
        else:
            pages = self.pages[page_start:page_stop]

        if type == "respond":
            response = self.basicqa(
                {"input_documents": pages, "question": question}, return_only_outputs=True
            )

        elif type == "mapreduce":
            response = self.map_reduce_chain({"input_documents": pages, "question": question})
        
        elif type == "refine":
            response = self.refine_chain({"input_documents": pages, "question": question})

        return response['output_text']
    
    def respond_guest(self, question, answer):
        return(self.refine_llm_chain.run(question = question, answer = answer))

    def respond_user(self, question, name, department, answer):
        return(self.refine_llm_pesornalizaed_chain.run(question = question, answer = answer, department = department, name = name))

    

def main():
    # print(os.environ['HF_TOKEN'])
    file_path = "Resource/Bells-Revised-Students-Handbook-Updated-version-1.pdf"
    llm_id = "mistralai/Mistral-7B-Instruct-v0.2"

    chat = HandBookChat(file_path, llm_id = llm_id)

    print("=================================================================")
    question = "What college am I in"
    answer = chat.respond(question, type = "refine").replace("\n", "")
    
    # print(chat.respond_guest(question, answer))
    print(chat.respond_user(question, "Lolade", "Mechatronics Engineering", answer))
    

if __name__ == '__main__':
	main()