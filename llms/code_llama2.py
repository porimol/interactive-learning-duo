from langchain.llms import CTransformers
from langchain.llms import LlamaCpp
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.vectorstores import Qdrant
from app.db.vectordb import RAG
from app.config import QDRANT_COLLECTION_NAME, CODE_LLAMA2


class CodeLlama2(RAG):
    """
    CodeLlama2 class represents a specific implementation of the RAG (Retrieval-Augmented Generation) model.

    Attributes:
        None

    Methods:
        __init__(): Initializes the CodeLlama2 object.
        __code_llama27b_llm(): Private method that creates and returns a CTransformers object for the CodeLlama-7B-Instruct-GGUF model.
        conversationa_chain_retrival(question, k=3): Retrieves the answer to a given question using a conversational retrieval chain.
        question_answer_retrieval(question, k=3): Retrieves and returns the answer to a given question using a retrieval-based question answering system.
    """
    def __init__(self):
        """
        Initializes the object.
        """
        super().__init__()

    def __code_llama27b_llm(self):
        """
        Creates and returns an instance of the CTransformers class with the specified parameters.

        Returns:
            CTransformers: An instance of the CTransformers class.
        """
        llm = CTransformers(
            model=CODE_LLAMA2,
            model_type="llama",
            temperature=0.0
        )
        # llm = LlamaCpp(
        #     model_path="/Users/chandp20/opt/Projects/UW/1st-semester/Intro2PythonAndSQL/project/pythonqa/llms/models/codellama-7b-instruct.Q4_K_M.gguf",
        #     temperature=0.10,
        #     n_ctx=3000,
        #     max_tokens=3000,
        #     n_gpu_layers=1,
        #     n_batch=512,
        #     f16_kv=True,
        #     # callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        #     verbose=False
        # )

        return llm
    
    def conversationa_chain_retrival(self, question, k=3):
        """
        Retrieves the answer to a given question using a conversational retrieval chain.

        Args:
            question (str): The question to be answered.

        Returns:
            dict: A dictionary containing the question and its corresponding answer.

        """
        custom_prompt_template = """
        Please use the given context to answer the question and please provide a precise answer according to the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Add comments in your answer for easy understanding.
        Always say thank you for asking question end of the answer.

        Context: {context}
        Question: {question}

        Answer:"""

        qa_rt_prompt = PromptTemplate(
            template=custom_prompt_template,
            input_variables=['context', 'question']
        )

        qa_rcr = ConversationalRetrievalChain.from_llm(
            self.__code_llama27b_llm(),
            retriever=self.vector_retriever(k),
            condense_question_prompt=qa_rt_prompt,
            rephrase_question=False
        )

        chat_history = []
        result_crc = qa_rcr({
            "question": question,
            "chat_history": chat_history
        })
        chat_history.append((question, result_crc["answer"]))
        response = {
            "question": question,
            "answer": result_crc["answer"]
        }
        return response
    
    def question_answer_retrieval(self, question, k=3):
        """
        Retrieves and returns the answer to a given question using a retrieval-based question answering system.
        The function uses a custom prompt template to guide the answering process. It retrieves relevant documents
        based on the question, and uses a Qdrant document store for retrieval. The function then creates a RetrievalQA
        object and uses it to generate the answer.

        Args:
            question (str): The question to be answered.

        Returns:
            RetrievalQA: The RetrievalQA object containing the answer to the question and the source documents used to generate the answer.
        """
        custom_prompt_template = """
        Please use the following context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Add comments in your answer for easy understanding and please provide a precise answer according to the question.
        Always say thank you for asking question end of the answer.

        Context: {context}
        Question: {question}

        Answer:"""

        qa_rt_prompt = PromptTemplate(
            template=custom_prompt_template,
            input_variables=['context', 'question']
        )

        doc_store = Qdrant(
            client=self.qdrant_client,
            collection_name=QDRANT_COLLECTION_NAME,
            embeddings=self.hf_embedding())

        rqa = RetrievalQA.from_chain_type(
            llm=self.__code_llama27b_llm(),
            chain_type='stuff',
            retriever=doc_store.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": k
                }
            ),
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": qa_rt_prompt
            }
        )
        result_rqa = rqa(question)

        response = {
            "question": question,
            "answer": result_rqa["answer"]
        }
        return response


if __name__ == "__main__":
    llm = CodeLlama2()
    question = "Write select SQLite query from users table."
    response = llm.conversationa_chain_retrival(question)
    print(f"{response['answer']}\n")

    question = "Write a pure Python code for addition and multiplication function"
    response = llm.conversationa_chain_retrival(question)
    print(f"{response['answer']}\n")

    question = "Write a python Employee class and add a full_name() method to return full name"
    response = llm.conversationa_chain_retrival(question)
    print(f"{response['answer']}\n")

