import psycopg2
import textwrap
from constants import *
from sqlalchemy import make_url
from llama_index.llms.groq import Groq
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, Settings, Document
# from llama_index import Document
from bs4 import BeautifulSoup
import os

def preprocess_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

# Lista para armazenar os documentos processados
documents = []

# Itera sobre os arquivos HTML no diretório
for filename in os.listdir(contents_dir):
    if filename.endswith(".html"):
        file_path = os.path.join(contents_dir, filename)
        text = preprocess_html(file_path)
        documents.append(Document(text=text))

# Exibe os documentos carregados
# for doc in documents:
#     print(doc.text)

##### SETUP LLM #####
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
Settings.llm = Groq(model="llama3-70b-8192")
# documents = SimpleDirectoryReader(contents_dir).load_data()

##### SETUP POSTGRES #####
conn = psycopg2.connect(connection_string)
conn.autocommit = True

with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")

##### CREATING THE INDEX #####
url = make_url(connection_string)
hybrid_vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name=table_name,
    embed_dim=embed_dim,
    hybrid_search=True,
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)

storage_context = StorageContext.from_defaults(vector_store=hybrid_vector_store)

hybrid_index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)