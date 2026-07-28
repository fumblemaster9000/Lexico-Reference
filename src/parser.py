import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    BSHTMLLoader,
    CSVLoader
    )
from langchain_core.documents import Document
import pytesseract
from pdf2image import convert_from_path

def read_file(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    #isolate the extension of the file [all lower case]
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension == ".pdf":
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        #Check if text is completley empty or too sparse
        total_text = "".join([doc.page_content for doc in documents])
        cleaned_text = "".join(total_text.split()) #Strip text of white space to trip OCR
        if len(cleaned_text) < 50: #less than 50 characters will prompt ocr
            print(f"Applying OCR to :{file_path}")
            ocr_output = []
            images = convert_from_path(file_path) #Convert each page of the pdf into a list
            for page_num, image in enumerate(images): #Loop through every page and keep track of pg#
                page_text = pytesseract.image_to_string(image)#run ocr on page image to extract text
                ocr_output.append(Document(page_content=page_text, metadata = {"source": file_path, "page": page_num}))
                #Compile extracted text into langchain document along with metadata
                #tracks source file and page index
            documents = ocr_output
            return documents
        

    elif extension == ".docx":
        loader = Docx2txtLoader(file_path)
    elif extension in [".txt", ".md"]:
        loader = TextLoader(file_path, encoding="utf-8")
    elif extension in [".html",".htm"]:
        loader = BSHTMLLoader(file_path)
    elif extension == ".csv":
            loader = CSVLoader(file_path)
    else:
        raise ValueError(f"Document extension {extension} is not recognized.")
    
    documents = loader.load()
    print(f"Successfully parsed {len(documents)} page(s) from {file_path}")
    return documents