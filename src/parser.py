import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
    )

def read_file(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    #isolate the extension of the file [all lower case]
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension == ".pdf":
        loader = PyPDFLoader(file_path)
    elif extension == ".docx":
        loader = Docx2txtLoader(file_path)
    elif extension in [".txt", ".md"]:
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Document extension {extension} is not recognized.")
    
    documents = loader.load()
    print(f"Successfully parsed {len(documents)} page(s) from {file_path}")
    return documents