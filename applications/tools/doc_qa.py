import datetime
import os

from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

PROMPT_TEMPLATE = """已知信息：
{context} 

根据上述已知信息，简洁和专业的来回答用户的问题。
如果无法从中得到答案，请说 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”，不允许在答案中添加编造成分，答案请使用中文。 
问题是：{question}"""


def load_file(filepath, chunk_size=500, chunk_overlap=0):
    if filepath.lower().endswith(".md"):
        loader = UnstructuredFileLoader(filepath, mode="elements")
        docs = loader.load()
    else:
        loader = UnstructuredFileLoader(filepath, mode="elements")
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "。", ".", " ", ""]
        )
        docs = loader.load_and_split(text_splitter=text_splitter)
    return docs


def init_knowledge_vector_store(embeddings, filepath: str, vs_path: str = None, **kwargs):
    docs = load_file(filepath, **kwargs)
    print("Initialized knowledge starting ...")
    if vs_path and os.path.isdir(vs_path):
        vector_store = FAISS.load_local(vs_path, embeddings)
        vector_store.add_documents(docs)
    else:
        if not vs_path:
            vs_path = f"""FAISS_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}"""
        vector_store = FAISS.from_documents(docs, embeddings)

    vector_store.save_local(vs_path)
    print("Initialized knowledge ended !")
    return vs_path


def generate_prompt(related_docs, query: str, prompt_template=PROMPT_TEMPLATE) -> str:
    context = "\n".join([doc.page_content for doc in related_docs])
    return prompt_template.replace("{question}", query).replace("{context}", context)


def get_related_docs(query, embeddings, vs_path, topk=3):
    vector_store = FAISS.load_local(vs_path, embeddings)
    related_docs_with_score = vector_store.similarity_search_with_score(query, k=topk)
    return related_docs_with_score