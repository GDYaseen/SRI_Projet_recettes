from langchain.text_splitter import RecursiveCharacterTextSplitter
import textwrap

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 0
    )
    texts = text_splitter.split_documents(documents)
    return texts



def wrap_text_preserve_newlines(text, width=700):
  lines = text.split('\n')

  wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
  wrapped_text = '\n'.join(wrapped_lines)
  return wrapped_text

def process_llm_response(llm_response):
  ans = wrap_text_preserve_newlines(llm_response['result'])

  sources_used = ' \n'.join(
        [
            source.metadata['source'].split('/')[-1][:-4] + ' - page: ' + str(source.metadata['page'])
            for source in llm_response['source_documents']
        ]
    )

  ans = ans + '\n\nSources: \n' + sources_used
  return ans


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