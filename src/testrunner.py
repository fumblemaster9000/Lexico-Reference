from parser import read_pdf

if __name__ == "__main__":
    test_pdf_path = "data/sample.pdf"
    
    docs = read_pdf(test_pdf_path)
    
    if docs:
        print("\n|Read and Check Data|")
        print(docs[0].page_content[:300]) # Prints the first 300 characters