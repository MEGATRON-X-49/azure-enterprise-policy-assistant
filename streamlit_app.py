import streamlit as st
import traceback

from app.ingestion import upload_pdf, extract_text_from_pdf
from app.retrieval import index_document
from app.chat import answer_question

st.set_page_config(
    page_title="Azure Enterprise Policy Assistant",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Azure Enterprise Policy Assistant")
st.caption("Ask questions about your uploaded company policies.")

# PDF upload
st.subheader("Upload Policy Document")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
)

if uploaded_file:
    if st.button("Upload and Process PDF"):
        with st.spinner("Uploading and processing document..."):
            try:
                upload_pdf(uploaded_file)

                pdf_bytes = uploaded_file.getvalue()
                pages = extract_text_from_pdf(pdf_bytes)

                chunk_count = index_document(
                    pages,
                    uploaded_file.name,
                )

                st.success(
                    f"Document processed successfully. "
                    f"{chunk_count} chunks indexed."
                )

            except Exception as e:
                st.error(f"Processing failed: {e}")
                st.exception(e)
                traceback.print_exc()

st.divider()

# Ask questions
st.subheader("Ask a Policy Question")

question = st.text_input(
    "Enter your question",
    placeholder="What is the company's leave policy?",
)

if st.button("Ask"):
    if question.strip():
        with st.spinner("Searching policy documents..."):
            try:
                answer = answer_question(question)
                st.markdown("### Answer")
                st.write(answer)

            except Exception as e:
                st.error(f"Unable to answer: {e}")
                st.exception(e)
                traceback.print_exc()
    else:
        st.warning("Enter a question first.")