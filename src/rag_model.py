from typing import Any
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
import os
from dotenv import load_dotenv


dataPath = os.path.abspath("data")

class Rag_model:
    def __init__(self):

        # Load environment variables from .env file
        load_dotenv()

        # Model and generation configuration
        self.model_name = "open-mixtral-8x7b"
        self.api_key = os.getenv('MISTRAL_API_KEY2')
        self.temperature = 0.1
        self.max_retries = 2
        self.max_new_tokens = 1024

        # Chunking and embeddings configuration
        self.split_chunk_size = 800
        self.split_overlap = 0
        self.k = 5

        # File paths
        self.PDFs_path = f"{dataPath}\\transcriptions"
        self.Embeddings_path = f"{dataPath}\\recipees_faiss_index_hp"
        self.Persist_directory = ""

        # Create ChatMistralAI instance
        print("Initializing ChatMistralAI...")
        self.llm = ChatMistralAI(
            model=self.model_name,
            api_key=self.api_key,
            temperature=self.temperature,
            max_retries=self.max_retries,
            max_new_tokens=self.max_new_tokens
        )


    def __call__(self):
        load_dotenv()
        return self.llm



# # Example usage
# if __name__ == "__main__":
#     rag_model = Rag_model()
#     llm = rag_model()
#     print("Model ready.")

