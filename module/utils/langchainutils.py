from langchain_community.document_loaders import PyPDFLoader

def extract_pdf(pdf_file):
  pdf_loader = PyPDFLoader(pdf_file)
  pages = pdf_loader.load_and_split()

  return pages

def load_prompt(text_file):
    f = open(text_file, "r")
    return f.read()
    
    
    