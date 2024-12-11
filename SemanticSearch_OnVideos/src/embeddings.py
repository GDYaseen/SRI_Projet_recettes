from helper_functions import *
import os
import logging
import time

from rag_model import *
from langchain_community.vectorstores import FAISS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingsManager:
    def __init__(self, pdfs):
        self.pdfs = pdfs
        # path where the vector database will be saved
        self.embeddings_path = 'D:/SemanticSearch_OnVideos/data/faiss_indexes'

        # Ensure the directory exists
        os.makedirs(self.embeddings_path, exist_ok=True)

        # Initialize embeddings model with error handling
        self.embeddings = MistralAIEmbeddings(
            model="mistral-embed",
            api_key='lCqBaCcz1kFirMMdnLdyEjQGAky9h9s9'
        )

    def batch_embed_with_retry(self, texts, batch_size=10, max_retries=3):
        """
        Embed texts in batches with retry mechanism to handle rate limiting
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            retry_count = 0

            while retry_count < max_retries:
                try:
                    batch_embeddings = self.embeddings.embed_documents(
                        [text.page_content for text in batch]
                    )
                    all_embeddings.extend(batch_embeddings)
                    break
                except Exception as e:
                    logger.warning(f"Embedding batch failed (attempt {retry_count + 1}): {e}")
                    retry_count += 1

                    if retry_count < max_retries:
                        # Exponential backoff
                        wait_time = (2 ** retry_count)
                        logger.info(f"Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                    else:
                        logger.error("Max retries reached. Embedding failed.")
                        raise

        return all_embeddings

    def load_vectordb(self):
        # Check if index files exist
        index_file = os.path.join(self.embeddings_path, 'index.faiss')

        # If index doesn't exist, create it
        if not os.path.exists(index_file):
            logger.info(f"Creating vector database at {self.embeddings_path}")

            # load data
            documents = load_documents(self.pdfs)

            # split texts
            texts = split_text(documents)

            # Debug: Print number of documents and text chunks
            logger.info(f"Total documents loaded: {len(documents)}")
            logger.info(f"Total text chunks: {len(texts)}")

            try:
                # Create embeddings and DB with custom batch embedding
                vectordb = FAISS.from_texts(
                    texts=[text.page_content for text in texts],
                    embedding=self.embeddings,
                    metadatas=[text.metadata for text in texts]
                )

                # persist vector database
                vectordb.save_local(self.embeddings_path)
                logger.info(f"Vector database created at {self.embeddings_path}")

            except Exception as e:
                logger.error(f"Vector database creation failed: {e}")
                raise

        # Load and return the vector database
        vectordb = FAISS.load_local(
            self.embeddings_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        return vectordb

    def __call__(self):
        # Return the embeddings model
        return self.embeddings
