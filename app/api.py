import os
import json
from fastapi import FastAPI
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAI
import warnings
warnings.filterwarnings('ignore')

with open('ignore/secret_key.json') as f:
    secret_key = json.load(f)['nvidia_key']

# Defines the Item class that inherits from BaseModel
class Item(BaseModel):
    query: str


# Sets the name of the model to be used to create the embeddings
model_name = "sentence-transformers/msmarco-bert-base-dot-v5"
model_kwargs = {'device': 'cpu'} # Model settings
encode_kwargs = {'normalize_embeddings': True} # Set encoding settings

# Initialize the HuggingFace embeddings class
hf = HuggingFaceEmbeddings(model_name = model_name,
                            model_kwargs = model_kwargs,
                            encode_kwargs = encode_kwargs)


# Set the use_nvidia_api variable to False
use_nvidia_api = False

# Verify if the Nvidia secret key is available
if secret_key != "":
    # Create an OpenAI instance with the base URL and API key
    client_ai = OpenAI(base_url = "https://integrate.api.nvidia.com/v1", api_key = secret_key)

    # Set use_nvidia_api to True
    use_nvidia_api = True

else:
    # Print a message indicating that an LLM cannot be used
    print("Unable to use an LLM.")
    

# Create an instance to connect to the vector database
client = QdrantClient("http://localhost:6333")
# Set the collection name
collection_name = "VectorDB"

# Creates an instance of Qdrant to send data to the vector database
qdrant = Qdrant(client, collection_name, hf)


# Create an instance
app = FastAPI()

# Set the root route with the GET method
@app.get("/")
async def root():
    return {"message": "RAG Project"}

# Define the /api route with the POST method
@app.post("/api")
async def api(item: Item):
    
    query = item.query # Get the query from the item
    search_result = qdrant.similarity_search(query = query, k = 10) # Perform the similarity search

    # Initialize the result list, context and mapping
    list_res = []
    context = ""
    mappings = {}

    # Construct the context and the list of results
    for i, res in enumerate(search_result):
        context += f"{i}\n{res.page_content}\n\n"
        mappings[i] = res.metadata.get("path")
        list_res.append({"id": i, "path": res.metadata.get("path"), "content": res.page_content})

    # Set the system message
    rolemsg = {"role": "system",
               "content": "Answer the user's question using documents provided in the context. The context contains documents that should contain an answer. Always reference the document ID (in square brackets, e.g. [0],[1]) of the document that was used to make a query. Use as many citations and documents as necessary to answer the question."}
    
    # Define messages 
    messages = [rolemsg, {"role": "user", "content": f"Documents:\n{context}\n\nQuestion: {query}"}]

    # Checks if Nvidia API is being used
    if use_nvidia_api:

        # Create LLM instance using Nvidia API
        response = client_ai.chat.completions.create(model = "meta/llama3-70b-instruct",
                                                     messages = messages,
                                                     temperature = 0.5,
                                                     top_p = 1,
                                                     max_tokens = 1024,
                                                     stream = False)
        # Get the response from LLM
        response = response.choices[0].message.content
    
    else:
        # Print a message indicating that an LLM cannot be used
        print("Unable to use an LLM.")
    
    return {"context": list_res, "answer": response}

