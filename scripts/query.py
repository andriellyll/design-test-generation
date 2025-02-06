import textwrap
from sqlalchemy import make_url
from constants import *
from llama_index.llms.groq import Groq
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, Settings

system_prompt = """ 
You are an assistant specialized in software engineering and design testing. 
Your task is to generate Java test case code using JUnit and Design Wizard to verify a given design rule.

## Instructions:
- You will receive a design rule as input.
- Your output should be only the corresponding Java test code, without any explanations.
- Use JUnit and Design Wizard to implement the test.

## Example:

### Input (Design Rule):
The `Strategy` pattern requires the context to use the `Strategy` interface, so concrete classes should never be referenced directly.

### Output (Java Test Code):
```java
@Test
    public void testContextOnlyKnowsStrategyInterface() throws Exception {
        DesignWizard dw = new DesignWizard("src/com/cnblog/clarck");
        ClassNode concreateStrategyA = dw.getClass("com.cnblog.clarck.ConcreateStrategyA");
        ClassNode concreateStrategyB = dw.getClass("com.cnblog.clarck.ConcreateStrategyB");
        ClassNode concreateStrategyC = dw.getClass("com.cnblog.clarck.ConcreateStrategyC");
        ClassNode strategyClass = dw.getClass("com.cnblog.clarck.Strategy");
        ClassNode context = dw.getClass("com.cnblog.clarck.Context");
        Set<ClassNode> calleeClasses = context.getCalleeClasses();

        assertTrue(calleeClasses.contains(strategyClass));
        assertFalse(calleeClasses.contains(concreateStrategyA));
        assertFalse(calleeClasses.contains(concreateStrategyB));
        assertFalse(calleeClasses.contains(concreateStrategyC));
    }
```
"""

##### SETUP LLM #####
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
Settings.llm = Groq(
    model="llama3-70b-8192",
    system_prompt=system_prompt   
)

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

query = "The concrete class needs to implement the `Strategy` interface to ensure that the `execute` method adheres to the defined contract."

hybrid_response = hybrid_query_engine.query(query)  
retrieved_docs = hybrid_query_engine.retrieve(query)
# Exibe os documentos retornados pelo retriever
print("\n🔍 DOCUMENTOS RECUPERADOS PELO RETRIEVER:\n")
for i, doc in enumerate(retrieved_docs):
    print(f"📄 Documento {i+1}:")
    print(doc.text)
    print("-" * 80)

print("RESPOSTA DO LLM:\n")
print(textwrap.fill(str(hybrid_response), 100))

