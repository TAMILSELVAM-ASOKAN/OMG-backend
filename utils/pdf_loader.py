from langchain_community.document_loaders import PyPDFLoader

def load_pdf(path: str) -> list[str]:
    loader = PyPDFLoader(path)
    docs = loader.load()
    return [d.page_content for d in docs]
