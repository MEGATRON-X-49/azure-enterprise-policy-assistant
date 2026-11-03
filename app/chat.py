from openai import AzureOpenAI

from app.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    CHAT_DEPLOYMENT,
)

from app.retrieval import search_documents


def get_openai_client():
    return AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )


def answer_question(question):
    documents = search_documents(question)

    if not documents:
        return "I couldn't find relevant information in the uploaded policy documents."

    context = ""

    for doc in documents:
        context += (
            f"\nSource: {doc['source']}, "
            f"Page: {doc['page']}\n"
            f"{doc['content']}\n"
        )

    client = get_openai_client()

    response = client.chat.completions.create(
        model=CHAT_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": """
You are an enterprise policy assistant.

Answer questions using ONLY the supplied policy document context.

Rules:
- Do not invent or assume policy information.
- If the context does not contain the answer, say:
  "I couldn't find this information in the uploaded policy documents."
- Cite the source filename and page number for factual claims.
- Keep answers clear and concise.
"""
            },
            {
                "role": "user",
                "content": f"""
Policy document context:
{context}

Question:
{question}
"""
            }
        ],
    )

    return response.choices[0].message.content