import uuid
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from app.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    EMBEDDING_DEPLOYMENT,
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_INDEX,
)


def get_openai_client():
    return AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )


def get_search_client():
    return SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX,
        credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
    )


def create_embedding(text):
    client = get_openai_client()

    response = client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=text,
    )

    return response.data[0].embedding


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def index_document(pages, filename):
    search_client = get_search_client()
    documents = []

    for page_data in pages:
        chunks = chunk_text(page_data["text"])

        for chunk in chunks:
            documents.append({
                "id": str(uuid.uuid4()),
                "content": chunk,
                "source": filename,
                "page": page_data["page"],
                "embedding": create_embedding(chunk),
            })

    if documents:
        search_client.upload_documents(documents=documents)

    return len(documents)
def search_documents(question, top_k=5):
    search_client = get_search_client()

    query_vector = create_embedding(question)

    results = search_client.search(
        search_text=question,
        vector_queries=[
            {
                "kind": "vector",
                "vector": query_vector,
                "fields": "embedding",
                "k": top_k,
            }
        ],
        select=["content", "source", "page"],
        top=top_k,
    )

    return [
        {
            "content": result["content"],
            "source": result["source"],
            "page": result["page"],
        }
        for result in results
    ]