

# Project Documentation: External Memory for LLM using RAG Techniques

## Overview
This project enhances the capabilities of a Large Language Model (LLM) by integrating external memory using **Retrieval-Augmented Generation (RAG)** techniques. The system allows the LLM to access and utilize external data stored in a vector database, enabling it to provide more informed, accurate, and contextually relevant responses. The project is structured using the **Poetry** package manager for dependency management and includes components for data processing, API creation, and a user-friendly web interface.

The system is designed to handle multiple file formats (txt, pdf, pptx, docx), process them into a standardized format, and store them in a **Qdrant** vector database. A **FastAPI** backend handles user prompts, retrieves relevant context from the database, and interacts with the **meta/llama3-70b-instruct** model hosted on the **Nvidia cloud**. A **Streamlit** web application provides an intuitive interface for users to interact with the system.

---

## Project Structure
The project is organized into the following directories and files:

```
.
├── README.md                   # Project documentation
├── data/                       # Directory containing external data files
├── poetry.lock                 # Poetry lock file for dependency versions
├── pyproject.toml              # Poetry project configuration file
├── app/                        # Application source code
│   ├── vectordb_rag.py         # Script for creating and managing the vector database
│   ├── api.py                  # FastAPI application for handling prompts and responses
│   ├── start_api.py            # Script to initialize the FastAPI server
│   └── webapp.py               # Streamlit web application for user interaction
└── notebooks/                  # Directory for exploratory analyses and notebooks
```

---

## Detailed Component Descriptions

### 1. `vectordb_rag.py`
This script is the backbone of the project, responsible for creating and managing the **Qdrant vector database**. It performs the following tasks:

#### Key Features:
- **Data Extraction**: Reads data from multiple file formats (txt, pdf, pptx, docx) located in the `data/` directory.
- **Data Transformation**: Processes the extracted data into a standardized format suitable for vectorization.
- **Vectorization**: Converts the processed data into embeddings using a pre-trained model.
- **Database Storage**: Stores the vectorized data in the Qdrant database for efficient similarity searches.

#### Workflow:
1. **Load Data**: Iterates through the `data/` directory and loads files based on their format.
2. **Transform Data**: Cleans and standardizes the data (e.g., removing special characters, splitting text into chunks).
3. **Generate Embeddings**: Uses a pre-trained embedding model to convert text into vectors.
4. **Store in Qdrant**: Saves the embeddings and metadata in the Qdrant database.


---

### 2. `api.py`
This file contains the **FastAPI** application that serves as the backend for the project. It handles user prompts, retrieves relevant context from the Qdrant database, and interacts with the LLM hosted on the Nvidia cloud.

#### Key Features:
- **Prompt Handling**: Accepts user prompts via an API endpoint.
- **Context Retrieval**: Searches the Qdrant database for the most relevant context based on the prompt.
- **Enhanced Prompt Creation**: Combines the original prompt with the retrieved context to create a detailed instruction for the LLM.
- **LLM Interaction**: Sends the enhanced prompt to the `meta/llama3-70b-instruct` model via the Nvidia cloud API.
- **Response Delivery**: Returns the LLM's response to the user.

#### Workflow:
1. **Receive Prompt**: The API accepts a prompt from the user.
2. **Retrieve Context**: Searches the Qdrant database for the most relevant context.
3. **Create Enhanced Prompt**: Combines the prompt and context into a detailed instruction.
4. **Send to LLM**: Sends the enhanced prompt to the LLM and waits for the response.
5. **Return Response**: Sends the LLM's response back to the user.


---

### 3. `start_api.py`
This script initializes the **FastAPI** server using the **Uvicorn** package. It is responsible for starting the API service that the web application interacts with.

#### Key Features:
- **Server Initialization**: Starts the FastAPI server on a specified port.
- **Asynchronous Support**: Uses `async` and `await` for efficient handling of requests.


---

### 4. `webapp.py`
This file contains the **Streamlit** web application that provides a user-friendly interface for interacting with the LLM. The web application is designed to be simple yet efficient, allowing users to enter prompts, view responses, and download source files.

#### Key Features:
- **Prompt Input**: A text input field for users to enter their prompts.
- **Response Display**: Displays the LLM's response to the entered prompt.
- **Source Download**: Provides an option to download the file from which the LLM retrieved the context for its response.

#### Workflow:
1. **User Input**: The user enters a prompt in the input field.
2. **Send to API**: The prompt is sent to the FastAPI backend for processing.
3. **Display Response**: The LLM's response is displayed on the screen.
4. **Download Source**: If applicable, the user can download the source file used for context retrieval.

---

## Setup and Installation

### Prerequisites
- Python 3.12 or higher
- Poetry package manager
- Qdrant (can be set up using Docker)
- Nvidia API key (for accessing the `meta/llama3-70b-instruct` model)

---
### Useful Links
* https://huggingface.co/meta-llama/Meta-Llama-3-70B/tree/main
* https://build.nvidia.com/meta/llama-3_3-70b-instruct

---
### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Krupique/rag-search
   cd rag-search
   ```

2. **Install Dependencies**:
   ```bash
   poetry install
   ```

3. **Set Up Qdrant**:
   - Ensure Qdrant is installed and running. You can use Docker to set up Qdrant:
    ```bash
    docker run --name vectordb -dit -p 6333:6333 qdrant/qdrant
    ```

4. **Add Data Files**:
   - Place your data files (txt, pdf, pptx, docx) in the `data/` directory.

5. **Initialize the Vector Database**:
   ```bash
   poetry run python app/vector_db.py data_path
   ```

6. **Start the FastAPI Server**:
   ```bash
   poetry run python app/start_api.py
   ```

7. **Run the Streamlit Web Application**:
   ```bash
   poetry run streamlit run app/webapp.py
   ```

P.S. The execution of webapp.py and start_api need to be in different bashes.

---

## Usage

### Accessing the Web Application
- Open your web browser and navigate to `http://localhost:8501` to access the Streamlit web interface.

### Interacting with the LLM
1. **Enter a Prompt**: Type your question or prompt into the input field.
2. **Submit**: Press the "Submit" button to send the prompt to the API.
3. **View Response**: The LLM's response will be displayed on the screen.
4. **Download Source**: If available, you can download the file from which the LLM retrieved the context.

---

### Example of prompts:
Questions:
* Was the Ninja 300 designed for rider-friendly?
* Have  the Ninja 250/300 won great popularity?

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Acknowledgments
- **Qdrant**: For providing the vector database solution.
- **FastAPI**: For enabling the creation of a robust and efficient API.
- **Streamlit**: For simplifying the development of the web interface.
- **Nvidia**: For hosting the `meta/llama3-70b-instruct` model.

---

## Contact
For any questions or feedback, please contact the project maintainer at [Henrique Krupck](krupck@outlook.com).

---

This detailed documentation provides a comprehensive guide to the project, its components, setup instructions, and usage guidelines. It is designed to help users and contributors understand and effectively utilize the system.
