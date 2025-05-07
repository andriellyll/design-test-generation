from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

prompt = """
Generate a set of sentences that define design rules for the **Builder pattern**, similar to the examples below. These rules should describe structural and behavioral constraints, focusing on:

- Relationships between **classes and packages**  
- Presence and usage of **methods and fields**  
- Constraints that enforce the **correct application of the pattern**

### Example Sentences:  
- SSL contexts shouldnt be reused across connections see So its probably more appropriate to pass in factories directly  
- To create a Finagle Thrift service you must implement the ServiceIface Interface that a custom Thrift compiler generates for your service Scrooge wraps your service method return values with asynchronous  
- I think its important to specify that the developer must implement ServiceIface and not Iface to make the example clearerisnotinvain that is a good idea  
- How about to create a Finagle Thrift service you must use the custom Thrift compiler which can be found here regular thrift Iface interface a ServiceIface interface that wraps all return values in a Future which is required by Finagle  

Generate additional sentences following this format, ensuring they clearly define the structure and rules of the **Builder pattern**.
"""
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(completion['choices'][0]['message']['content'])