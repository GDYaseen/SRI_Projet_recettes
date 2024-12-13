import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import textwrap

import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 0
    )
    texts = text_splitter.split_documents(documents)
    return texts


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

vidsPath = os.path.abspath("data/videos").replace("\\","/")+"/"

def wrap_text_preserve_newlines(text, width=700):
  lines = text.split('\n')

  wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
  wrapped_text = '\n'.join(wrapped_lines)
  return wrapped_text

def process_llm_response(llm_response):
  ans = wrap_text_preserve_newlines(llm_response['result'])

  sources_used = list(
        {"data/videos/"+source.metadata['source'].replace("\\","/").split('/')[-1].replace("_transcription", "").split('.')[0]+".mp4"
         for source in llm_response['source_documents']}
    )

  return {
        "description": ans,
        "sources": sources_used
    }


def load_documents(pdfs_path):
    try:
        loader = DirectoryLoader(
            pdfs_path,
            glob="./*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True,
            use_multithreading=True
        )

        documents = loader.load()

        if not documents:
            logger.warning(f"No documents found in {pdfs_path}")

        return documents
    except Exception as e:
        logger.error(f"Error loading documents from {pdfs_path}: {e}")
        raise