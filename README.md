# rag-search


This project focuses on developing the second part of an intelligent document search system using Generative AI and Large Language Models (LLMs). We will build the frontend to allow users to query internal company documents (TXT, PDF, DOCX, PPTX) and receive AI-generated responses. The system leverages Retrieval-Augmented Generation (RAG) to enhance the accuracy and relevance of search results.

## Useful links

* https://huggingface.co/meta-llama/Meta-Llama-3-70B/tree/main
* https://build.nvidia.com/meta/llama-3_3-70b-instruct

## Hot to run
```bash
poetry install
```
```bash
docker run --name vectordb -dit -p 6333:6333 qdrant/qdrant
```

```bash
poetry run python app/vector_db.py
```

```bash
poetry run python app/start_api.py
```

```bash
poetry run streamlit run app/webapp.py
```
