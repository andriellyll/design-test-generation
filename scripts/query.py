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

def get_system_prompt(class_structure):
    return  f""" 
    You are an assistant specialized in software engineering and design testing.  
    Your task is to generate **Java test case code** using **JUnit and Design Wizard** to verify a given design rule.

    ## **Instructions**:
    - You will receive **three inputs**:
    1. A **design rule** that needs to be verified.
    2. A **compiled class structure** (generated using `javap`) that describes the system.
    3. Extracted documentation from the **Design Wizard** library.

    - **Follow a step-by-step reasoning process** to determine the best way to verify the rule before generating the test code.

    - Your final output should **only contain the Java test code** (without explanations), but follow this internal reasoning process before producing the output:

    ## **Reasoning Process**:

    1. **Analyze the Design Rule**  
    - Carefully read and understand the rule that needs to be enforced.  
    - Identify what relationships or constraints must be tested.

    2. **Examine the System Summary (Compiled Class Structure)**  
    - Use the provided class definitions to **map out** the system structure.
    - Identify **classes, methods, fields, and inheritance/composition** relationships.
    - Determine **which classes and methods are relevant** to enforcing the design rule.

    3. **Extract Relevant Information from the Documentation**  
    - Focus only on the **Design Wizard** methods/classes that help enforce the rule.
    - Identify how Design Wizard can be used to analyze relationships between classes.

    4. **Define the Test Strategy**  
    - Determine **which classes, methods, or interactions** should be tested.
    - Decide **which assertions** will verify compliance with the design rule.

    5. **Generate the Java Test Code**  
    - Implement the test using **JUnit and Design Wizard**.
    - Ensure the test correctly verifies adherence to the design rule.

    ## Compiled Class Structure:

    ```
    {class_structure}
    ```

    ## **Example**:

    ### **Input (Design Rule)**:
    > The `Strategy` pattern requires the context to use the `Strategy` interface,  
    > so concrete classes should never be referenced directly.

    ### **Output (Java Test Code)**:
    ```java
    @Test
    public void testContextOnlyKnowsStrategyInterface() throws Exception {{
        # You can assume that the directory that contains the .class files is always "bin"
        DesignWizard dw = new DesignWizard("bin");
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
    }}
    ```

    In this example, the relevant documentation from **Design Wizard** includes:
    - How to retrieve a **ClassNode** for a given class.
    - How to get the **callee classes** of a given class.
    """

rules_strategy = [
    "Each strategy must implement the `algorithmInterface` method defined in the abstract class.",
    "The `Strategy` abstract class was designed to be stateless, so avoid adding state attributes to its implementations.",
    "The concrete class needs to extend the `Strategy` abstract class to ensure that the `algorithmInterface` method adheres to the defined contract.",
    "Each concrete implementation must encapsulate a single algorithm and be completely independent of the other strategies.",
    "The Strategy abstract class should define a single method representing the algorithm to be executed, keeping the contract simple and consistent."
]

rules_facade = [
    "Only the `Facade` class should directly interact with the subsystems — all other classes must interact exclusively through the `Facade`.",
    "The `Facade` class should be aware of the internal subsystems, but the subsystems should not depend on or have knowledge of the `Facade`.",
    "The internal classes that compose the subsystems must not be directly accessible outside the package — this reinforces the use of the `Facade`.",
    "A Facade should be implemented as a concrete class, not an interface, since it represents a fixed entry point to a subsystem.",
    "The Facade should only expose methods necessary for client interactions, keeping its API minimal to reduce coupling."
]

rules_simple_factory = [
    "All objects created by the `Simple Factory` must implement or inherit from a common interface or base class.",
    "The client must call the `Simple Factory` to create objects and not use the `new` operator directly.",
    "The factory class must not store created instances.",
    "Each product class should be independent and unaware of the factory, ensuring that modifications to the factory do not affect product implementations.",
    "The factory method should return instances of concrete product classes but expose them only through their common interface or superclass."
]

rules_composite = [
    "Every component, whether it’s a leaf or a composite, must extend the Component abstract class to ensure consistent behavior.",
    "Make sure the leaf nodes don’t have any children — their methods should operate as if they are the end of the hierarchy.",
    "Instead of exposing direct references to child nodes, the composite should provide methods to manage children, like add, remove, or getChild.",
    "Leaf nodes must not contain references to other components, as they represent indivisible elements in the hierarchy.",
    "Avoid introducing direct dependencies between Composite and concrete Leaf implementations to preserve flexibility when extending the hierarchy."
]

rules_adapter = [
    "The Adapter class must extend the target class so the client can interact with it seamlessly.",
    "Use composition instead of inheritance in the Adapter to wrap the adaptee, keeping the two classes loosely coupled.",
    "The Adapter should expose only the methods defined in the target class, even if the adaptee has additional functionality.",
    "The Adapter should delegate all calls to the Adaptee, converting method signatures and data formats as needed.",
    "Avoid exposing the Adaptee directly to the client, as this breaks encapsulation and defeats the purpose of the Adapter."
]

rules = [
    "Each Concrete Builder should extend the Builder abstract class and provide specific implementations for constructing parts of the product.",
    "The product class should be independent of the Builder — the Builder is responsible for assembling the product, but the product doesn’t know about the Builder.",
    "Avoid tightly coupling the Director to a specific Builder — it should only know about the Builder class.",
    "The final product should only be accessible through a getResult() method, preventing incomplete object creation.",
    "The Builder and the Product class should be placed in the same package to restrict direct instantiation while allowing controlled access."
]

class_structure = """
Compiled from "Client.java"
public class com.cnblog.clarck.Client {
  public com.cnblog.clarck.Client();
  public static void main(java.lang.String[]);
}
Compiled from "Builder.java"
public abstract class com.cnblog.clarck.Builder {
  public com.cnblog.clarck.Builder();
  public abstract void buildPartA();
  public abstract void buildPartB();
  public abstract com.cnblog.clarck.Product getResult();
}
Compiled from "ConcrateBuilder2.java"
public class com.cnblog.clarck.ConcrateBuilder2 extends com.cnblog.clarck.Builder {
  private com.cnblog.clarck.Product product;
  public com.cnblog.clarck.ConcrateBuilder2();
  public void buildPartA();
  public void buildPartB();
  public com.cnblog.clarck.Product getResult();
}
Compiled from "Director.java"
public class com.cnblog.clarck.Director {
  public com.cnblog.clarck.Director();
  public void Construct(com.cnblog.clarck.Builder);
}
Compiled from "Product.java"
public class com.cnblog.clarck.Product {
  private java.util.List<java.lang.String> parts;
  public com.cnblog.clarck.Product();
  public void add(java.lang.String);
  public void show();
}
Compiled from "ConcrateBuilder1.java"
public class com.cnblog.clarck.ConcrateBuilder1 extends com.cnblog.clarck.Builder {
  private com.cnblog.clarck.Product product;
  public com.cnblog.clarck.ConcrateBuilder1();
  public void buildPartA();
  public void buildPartB();
  public com.cnblog.clarck.Product getResult();
}
""" 
system_prompt = get_system_prompt(class_structure)

##### SETUP LLM #####
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
# Settings.llm = Groq(
#     model="llama3-70b-8192",
    # system_prompt=system_prompt   
# )

Settings.llm = MistralAI(
    model="codestral-latest",
    temperature=0.1,
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

