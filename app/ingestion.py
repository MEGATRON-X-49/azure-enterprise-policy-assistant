import fitz
from azure.storage.blob import BlobServiceClient
from app.config import (
    AZURE_STORAGE_CONNECTION_STRING,
    AZURE_STORAGE_CONTAINER,
)


def get_container_client():
    blob_service = BlobServiceClient.from_connection_string(
        AZURE_STORAGE_CONNECTION_STRING
    )
    return blob_service.get_container_client(
        AZURE_STORAGE_CONTAINER
    )


def upload_pdf(file):
    container = get_container_client()
    blob_client = container.get_blob_client(file.name)

    blob_client.upload_blob(file, overwrite=True)

    return blob_client.url


def extract_text_from_pdf(pdf_bytes):
    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()

        if text.strip():
            pages.append({
                "page": page_number,
                "text": text
            })

    document.close()
    return pages