# Azure Enterprise Policy Assistant

A document-based question-answering application built using Python and Microsoft Azure. It allows users to upload employee policy documents in PDF format and ask questions about their contents through a simple web interface.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate answers grounded in the retrieved content, with references to the source document and page number.

## Project Overview

Company policy documents often contain information spread across multiple pages, making it difficult to locate specific details quickly.

This application addresses that problem by allowing users to upload policy PDFs and ask questions in natural language. Instead of relying solely on the language model's existing knowledge, it retrieves relevant sections from the uploaded documents and uses them as context when generating responses.

When the requested information is not available in the documents, the application responds accordingly rather than generating an unsupported answer.

## Features

- Upload PDF documents through a Streamlit interface.
- Store uploaded documents in Azure Blob Storage.
- Extract document text using PyMuPDF.
- Split extracted text into overlapping chunks.
- Generate embeddings using Azure OpenAI.
- Index document content and embeddings in Azure AI Search.
- Retrieve relevant content using vector search.
- Generate context-grounded responses using GPT-5-mini.
- Display source filenames and page references.
- Handle questions that cannot be answered using the available documents.

## Architecture

The application follows a Retrieval-Augmented Generation workflow consisting of two main processes.

### Document Ingestion

1. The user uploads a PDF through the Streamlit interface.
2. The document is stored in Azure Blob Storage.
3. PyMuPDF extracts text from the PDF.
4. Extracted text is divided into smaller chunks with overlapping content.
5. Azure OpenAI generates embeddings for each chunk using `text-embedding-3-small`.
6. The chunks, embeddings and document metadata are stored in Azure AI Search.

### Question Answering

1. The user submits a question through the application.
2. Azure OpenAI generates an embedding for the question.
3. Azure AI Search retrieves the most relevant document chunks.
4. The retrieved content is passed to GPT-5-mini as context.
5. The model generates an answer based on the retrieved information.
6. The application displays the answer with source document and page references.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Application development |
| Streamlit | Web interface |
| Azure OpenAI GPT-5-mini | Answer generation |
| text-embedding-3-small | Embedding generation |
| Azure AI Search | Vector search and retrieval |
| Azure Blob Storage | Document storage |
| PyMuPDF | PDF text extraction |
| Azure SDK for Python | Azure service integration |

## Project Structure

```text
azure-enterprise-policy-assistant/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion.py
│   ├── retrieval.py
│   ├── chat.py
│   └── search_setup.py
│
├── streamlit_app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.12
- An Azure subscription
- Azure OpenAI resource with chat and embedding deployments
- Azure AI Search service
- Azure Storage account

### 1. Clone the repository

```bash
git clone https://github.com/MEGATRON-X-49/azure-enterprise-policy-assistant.git

cd azure-enterprise-policy-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Azure credentials

Create a `.env` file in the project root directory:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_API_VERSION=2024-10-21

AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-5-mini-1
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small

AZURE_STORAGE_CONNECTION_STRING=
AZURE_STORAGE_CONTAINER=policy-documents

AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_API_KEY=
AZURE_SEARCH_INDEX=policy-index
```

Populate the variables with the credentials and endpoints from your Azure resources.

Do not commit the `.env` file or expose Azure credentials.

### 5. Create the Azure AI Search index

```powershell
python -c "from app.search_setup import create_search_index; print(create_search_index())"
```

### 6. Run the application

```bash
streamlit run streamlit_app.py
```

Open the application in your browser:

`http://localhost:8501`

Upload a PDF document to begin asking questions about its contents.

## Testing

The application was tested using a sample employee policy handbook containing information about annual leave, sick leave, remote work, expense reimbursement and workplace policies.

The following scenarios were verified:

- PDF upload and storage in Azure Blob Storage.
- Text extraction and document chunking.
- Embedding generation through Azure OpenAI.
- Document indexing in Azure AI Search.
- Retrieval of relevant document sections.
- Answer generation using retrieved context.
- Source document and page references in responses.
- Handling of questions whose answers are not present in the uploaded documents.

## Author

**Kamal Mudiraj**

