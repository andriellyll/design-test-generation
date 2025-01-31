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

query = "How could I print all methods of a class using the Design Wizard library?"

hybrid_response = hybrid_query_engine.query(
    """
        Generate a test case code using JUnit and Design Wizard to verify the following rule:
        - The `Strategy` interface was designed to be stateless, so avoid adding state attributes to its implementations.

        Example:
            Rule:
                The concrete class needs to implement the `Strategy` interface to ensure that the `execute` method adheres to the defined contract.
            Code:
                @Test
                public void testConcreteImplementsStrategy() throws Exception {
                    DesignWizard dw = new DesignWizard("src/com/cnblog/clarck");
                    ClassNode classNode = dw.getClass("com.cnblog.clarck.ConcreateStrategyA");
                    ClassNode classNode2 = dw.getClass("com.cnblog.clarck.Strategy");
                    assertTrue(classNode.extendsClass(classNode2));
                }
    """
)   

# Exibe os documentos retornados pelo retriever
# print("\n🔍 DOCUMENTOS RECUPERADOS PELO RETRIEVER:\n")
# for i, doc in enumerate(retrieved_docs):
#     print(f"📄 Documento {i+1}:")
#     print(doc.text)
#     print("-" * 80)

# # Agora, passa para o LLM gerar a resposta
# hybrid_response = hybrid_query_engine.query(query)

# # Exibe a resposta final
# print("\n🤖 RESPOSTA DO LLM:\n")
# print(textwrap.fill(str(hybrid_response), 100))

print(textwrap.fill(str(hybrid_response), 100))


# Perguntas úteis para teste:
#   What means 'Keep the core clean' in prism?
#   Which Java version should be used to create a new service in bom?
#   Describe how can I onboard a new service in bom
#   What can the user search in the search pane?