import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from src.pipeline import rag_pipeline

if __name__ == "__main__":
    print("Starting LEXICO-REFERENCE RAG Pipeline...")
    
    #Initialize
    chain = rag_pipeline(file_path = "data", persist_dir="chroma_db")
    
    print("\nPipeline Ready, type 'exit' or 'quit' to stop. \n")
    
    while True:
        try:
            question = input("USER: ").strip()
            if not question:
                continue
            if question.lower() in ["exit", "quit"]:
                print("Exiting pipeline.")
                break
            
            print("\nThinking...")
            response = chain.invoke(question)
            print(f"\nAnswer: \n{response}\n" + "-"*50)
            
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break
        except Exception as e:
            print(f"\nError: {e}\n" + "-"*50)