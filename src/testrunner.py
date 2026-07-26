from parser import read_file

if __name__ == "__main__":
    
    #pdf test
    test_pdf_path = "data/sample.pdf"
    docs = read_file(test_pdf_path)
    if docs:
        print("\n|Read and Check Data|")
        print(docs[0].page_content[:300]) # Prints the first 300 characters
    
    #docx test
    test_pdf_path = "data/file-sample_100kB.docx"
    docs = read_file(test_pdf_path)
    if docs:
            print("\n|Read and Check Data|")
            print(docs[0].page_content[:300]) # Prints the first 300 characters
            
    #txt test
    test_pdf_path = "data/example.txt"
    docs = read_file(test_pdf_path)
    if docs:
            print("\n|Read and Check Data|")
            print(docs[0].page_content[:300]) # Prints the first 300 characters