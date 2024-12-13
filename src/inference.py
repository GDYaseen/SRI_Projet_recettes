from src.rag_model import *
from src.embeddings import *
from src.helper_functions import process_llm_response, wrap_text_preserve_newlines
import time
from langchain.chains import RetrievalQA
import langchain
# prompts
from langchain_core.prompts import PromptTemplate

# Temporary fix for OpenMP runtime conflict
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


#TODO: add the path to the pdfs
pdfs = os.path.abspath("data/transcriptions")

class Inference:
    def __init__(self):
        self.prompt_template = """[INST] You are given the context after <> and a question after <>.

Answer the question by only using the information in context. Only base your answer on the information in the context. Even if you know something more,
keep silent about it. It is important that you only tell what can be infered from the context alone.even if you know the answer only use what is provided in the context.

<>{question}\n<>{context} [/INST]"""
        self.embeddings_manager = EmbeddingsManager(pdfs)
        self.retriever = self.embeddings_manager.load_vectordb().as_retriever(search_kwargs =
                                  {"k":5, "search_type":"similarity"})
        self.llm = Rag_model()

        self.qa_chain = self._initialize_qa_chain()

    def _initialize_qa_chain(self):
        PROMPT = PromptTemplate(
            template = self.prompt_template,
            input_variables = ["question", "context"]
        )
        return RetrievalQA.from_chain_type(
            llm = self.llm(),
            chain_type = "stuff",
            retriever = self.retriever,
            chain_type_kwargs = {"prompt":PROMPT},
            return_source_documents = True,
            verbose = False
        )

    def llm_ans(self, query):
        start = time.time()
        llm_response = self.qa_chain.invoke(query)
        processed_response =process_llm_response(llm_response)
        end = time.time()

        time_elapsed = int(round(end - start, 0))
        processed_response["time_elapsed"] = f"{time_elapsed}s"
        return processed_response

    def __call__(self, query):
        return self.llm_ans(query)