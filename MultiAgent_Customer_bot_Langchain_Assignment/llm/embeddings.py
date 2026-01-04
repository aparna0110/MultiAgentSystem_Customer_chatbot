from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embeddings():
    """
    Returns Hugging Face embedding model.
    No API keys required.
    """

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )