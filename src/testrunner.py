from parser import read_file
from splitter import split_text

if __name__ == "__main__":
    
    #pdf test
    test_pdf_path = "data/sample.pdf"
    docs = read_file(test_pdf_path)
    if docs:
        print("\n|Read and Check Data|")
        print(f"Loaded {len(docs)} page(s).")
        
        chunks = split_text(docs, chunk_size=500, chunk_overlap=50)
        
        print("\n|Chunking Check|")
        print(f"Total chunks: {len(chunks)}")
        print("\nFirst Chunk Sample:")
        
        print(docs[0].page_content[:300]) # Prints the first 300 characters
    
    #docx test
    test_pdf_path = "data/file-sample_100kB.docx"
    docs = read_file(test_pdf_path)
    if docs:
            print("\n|Read and Check Data|")
            print(f"Loaded {len(docs)} page(s).")
            
            chunks = split_text(docs, chunk_size=500, chunk_overlap=50)
            
            print("\n|Chunking Check|")
            print(f"Total chunks: {len(chunks)}")
            print("\nFirst Chunk Sample:")
            
            print(docs[0].page_content[:300])
            
    #txt test
    test_pdf_path = "data/example.txt"
    docs = read_file(test_pdf_path)
    if docs:
            print("\n|Read and Check Data|")
            print(f"Loaded {len(docs)} page(s).")
            
            chunks = split_text(docs, chunk_size=500, chunk_overlap=50)
            
            print("\n|Chunking Check|")
            print(f"Total chunks: {len(chunks)}")
            print("\nFirst Chunk Sample:")
            
            print(docs[0].page_content[:300])