import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv  

load_dotenv()

def get_llm(temperature: float = 0.0, max_tokens: int | None=None) -> AzureChatOpenAI:
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_api_base = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

    llm = AzureChatOpenAI(
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=azure_api_key,
        azure_endpoint=azure_api_base,
        api_version=azure_api_version,
        azure_deployment=azure_deployment_name,
    )
    return llm

if __name__ == "__main__":
    llm = get_llm(temperature=0.7, max_tokens=150)
    response = llm.invoke("Hello, how are you?")
    print(response)
