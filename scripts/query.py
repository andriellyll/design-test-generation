import textwrap
from sqlalchemy import make_url
from constants import *
from llama_index.llms.groq import Groq
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, Settings

##### SETUP LLM #####
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
Settings.llm = Groq(model="llama3-70b-8192")

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

hybrid_index = VectorStoreIndex.from_vector_store(vector_store=hybrid_vector_store)

hybrid_query_engine = hybrid_index.as_query_engine(
    vector_store_query_mode = "hybrid", sparse_top_k=2
)

hybrid_response = hybrid_query_engine.query(
    "How could I print all methods of a class using the Design Wizard library?"
)
print(textwrap.fill(str(hybrid_response), 100))


# Perguntas úteis para teste:
#   What means 'Keep the core clean' in prism?
#   Which Java version should be used to create a new service in bom?
#   Describe how can I onboard a new service in bom
#   What can the user search in the search pane?