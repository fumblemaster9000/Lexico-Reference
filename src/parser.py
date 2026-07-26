#PDF reader function
from langchain_community.document_loaders import PyPDFLoader

def read_pdf(file_path: str): #function definition
    pdf_loader = PyPDFLoader(file_path) #Tool initilization
    raw_documents = pdf_loader.load()
    
    print(f"Succesfully read {len(raw_documents)} pages from the PDF.")
    return raw_documents