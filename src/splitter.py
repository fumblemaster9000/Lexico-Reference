from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(documents, chunk_size = 500, chunk_overlap = 50):
    #Takes text and splits it into chunks using langchain recursive character text splitter
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
        is_separator_regex=False, #treat seperators as normal text
        )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Successfully split {len(documents)} page(s) into {len(chunks)} chunk(s)")
    return chunks