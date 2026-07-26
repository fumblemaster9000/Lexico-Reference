from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(documents, chunk_size = 1000, chunk_overlap = 100): #default values
    #Takes text and splits it into chunks using langchain recursive character text splitter
    #Optimized for dictionary and lexicon structures, the program prioritizes paragraph and line boundaries
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        separators=[
            "\n\n\n", #Major Section Breaks
            "\n\n", #Paragraph Boundaries
            "\n", #Line Breaks
            "", #Word fallback
            "" #Character fallback
            ],
        keep_separator = True
        )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Successfully split {len(documents)} page(s) into {len(chunks)} chunk(s)")
    return chunks