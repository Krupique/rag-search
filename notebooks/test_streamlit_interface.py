import re
import streamlit as st
import requests
import json
import warnings

warnings.filterwarnings('ignore')

# Setting the page title and other settings (favicon)
st.set_page_config(page_title="RAG Project", page_icon=":100:", layout="centered")

# Sets the title of the Streamlit application
st.title('_:green[RAG Project]_')
st.title('_:blue[Search using Generative AI and RAG]_')

# Creates a text box for question input
question = st.text_input("Type a Question for AI to Query Documents:", "")


if st.button("Send"): # Check if the "Ask" button was clicked
    st.write("The question was: \"", question+"\"")
    
    url = "http://127.0.0.1:8000/api" # Define the API URL
    
    payload = json.dumps({"query": question}) # Create the request payload in JSON format
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'} # Set the request headers
    
    response = requests.request("POST", url, headers=headers, data=payload) # Make the POST request to the API

    # Get the response from the API and extract the text from the answer to the question
    answer = json.loads(response.text)["answer"]
    
    # Compile a regular expression to find references to documents
    rege = re.compile("\[Document\ [0-9]+\]|\[[0-9]+\]")
    
    # Find all references to documents in the response
    m = rege.findall(answer)
    
    # Initialize a list to store document numbers
    num = []
    
    # Extract document numbers from found references
    for n in m:
        num = num + [int(s) for s in re.findall(r'\b\d+\b', n)]

    # Display the question answer using markdown
    st.markdown(answer)
    
    # Get the documents from the response context
    documents = json.loads(response.text)['context']
    
    # Initialize a list to store the documents that will be displayed
    show_docs = []
    
    # Add the documents corresponding to the extracted numbers to the show_docs list
    for n in num:
        for doc in documents:
            if int(doc['id']) == n:
                show_docs.append(doc)
                
    # Initialize a variable for the download buttons identifier
    id = 1
    
    # Displays expanded documents with download buttons
    for doc in show_docs:
        
        # Creates an expander for each document
        with st.expander(str(doc['id'])+" - "+doc['path']):
            
            # Displays the contents of the document
            st.write(doc['content'])
            
            # Opens the document file and creates a download button
            with open(doc['path'], 'rb') as f:
                
                st.download_button("Download do Arquivo", f, file_name = doc['path'].split('/')[-1], key = id)
                
                # Increments the download button identifier
                id = id + 1
