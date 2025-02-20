import textwrap
from sqlalchemy import make_url
from constants import *
from llama_index.llms.groq import Groq
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, Settings
from dotenv import load_dotenv
from llama_index.llms.mistralai import MistralAI
import pandas as pd
import time
from datetime import datetime

load_dotenv()

system_prompt = """ 
You are an assistant specialized in software engineering and design testing.  
Your task is to generate **Java test case code** using **JUnit and Design Wizard** to verify a given design rule.

## **Instructions**:
- You will receive a **design rule** as input.
- You will also receive **extracted documentation** from the **Design Wizard** library.
- **Follow a step-by-step reasoning process** to determine the best way to verify the rule before generating the test code.
- Your final output should **only contain the Java test code** (without explanations), but follow this internal reasoning process before producing the output:

## **Reasoning Process**:
1. **Understand the Design Rule**  
   - Analyze the given design rule carefully.  
   - Identify what needs to be **enforced** or **restricted** in the code.

2. **Extract Relevant Information from the Documentation**  
   - Focus only on the parts of the Design Wizard documentation that **directly help** enforce the given rule.  
   - Identify the key methods/classes in Design Wizard that should be used.

3. **Define the Test Strategy**  
   - Determine the **classes, methods, or relationships** that need to be verified.  
   - Decide which assertions should be used to check compliance with the design rule.

4. **Generate the Java Test Code**  
   - Implement the JUnit test using Design Wizard.  
   - Ensure the test effectively enforces the rule.

## **Example**:

### **Input (Design Rule)**:
> The `Strategy` pattern requires the context to use the `Strategy` interface,  
> so concrete classes should never be referenced directly.

### **Output (Java Test Code)**:
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

In this example, the relevant documentation from **Design Wizard** includes:
- How to retrieve a **ClassNode** for a given class.
- How to get the **callee classes** of a given class.
"""

##### SETUP LLM #####
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
# Settings.llm = Groq(
#     model="llama3-70b-8192",
#     system_prompt=system_prompt   
# )

Settings.llm = MistralAI(
    model="codestral-latest",
    system_prompt=system_prompt,
    temperature=0.1
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

df = pd.read_csv('dataset.csv')
rules = df["Texto"]

# query = "The concrete class needs to implement the `Strategy` interface to ensure that the `execute` method adheres to the defined contract."

# query = "Avoid tightly coupling the Director to a specific Builder — it should only know about the Builder interface."

    # retrieved_docs = hybrid_query_engine.retrieve(rule)
    
    # print("\nDOCUMENTOS RECUPERADOS PELO RETRIEVER:\n")
    # for i, doc in enumerate(retrieved_docs):
    #     print(f"Documento {i+1}:")
    #     print(doc.text)
    #     print("-" * 80)
date_now = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f"saida-{date_now}.txt"

with open(output_file, "w") as f:
    pass

for rule in rules:
    print(f"Gerando código para regra: {rule}")
    hybrid_response = hybrid_query_engine.query(rule)  

    print("\nRESPOSTA DO LLM:")
    print("-" * 80)  # Linha separadora
    print(str(hybrid_response))
    print("-" * 80)  # Linha separadora
    print("\n")
    
    with open(output_file, "a") as f:
        f.write("-" * 60)
        f.write(f"\nRESPOSTA PARA REGRA {rule}\n")
        f.write("-" * 60)
        f.write(f"\n{str(hybrid_response)}\n\n\n\n")
        

    time.sleep(30)

