from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from llm.embeddings import get_embeddings

# Temporary in-memory store (can replace with Azure AI Search later)
_vector_store = None


def load_faq_vector_store():
    global _vector_store

    if _vector_store:
        return _vector_store

    embeddings = get_embeddings()

    faq_data = [
    {
        "question": "How do I reset my password?",
        "answer": "You can reset your password using the Forgot Password option."
    },
    {
        "question": "How to update my email?",
        "answer": "Go to profile settings and update your email."
    }
]

    documents = []

    for item in faq_data:
        text = f"Question: {item['question']}\nAnswer: {item['answer']}"
        documents.append(
            Document(page_content=text)
        )
    print("documents type ++++++++++++++++",type(documents[0].page_content))

    return FAISS.from_documents(documents, embeddings)

    # docs = [
    #     Document(page_content="You can reset your password using the Forgot Password option."),
    #     Document(page_content="Refunds are processed within 5-7 business days."),
    #     Document(page_content="Insurance claims require valid documents for approval.")
    # ]

    # _vector_store = FAISS.from_documents(docs, embeddings)
    # return _vector_store
