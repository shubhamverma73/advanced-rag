from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader

from pinecone import Pinecone

from dotenv import load_dotenv
import os

load_dotenv()

# -----------------------------
# Load PDF
# -----------------------------
loader = PyPDFLoader("data/environment_policy.pdf")
#loader = PyPDFLoader("data/hr_policy.pdf")
#loader = PyPDFLoader("data/safety_manual.pdf")
documents = loader.load()

# -----------------------------
# Chunking
# -----------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)

chunks = splitter.split_documents(documents)

print(f"Total Chunks : {len(chunks)}")

# -----------------------------
# Embedding Model
# -----------------------------
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# -----------------------------
# Pinecone
# -----------------------------
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.index("simple-rag-md")

# -----------------------------
# Prepare Documents
# -----------------------------
pinecone_docs = []

for i, chunk in enumerate(chunks):

    vector = embeddings.embed_query(chunk.page_content)

    pinecone_docs.append(
        {
            "_id": f"chunk-{i}",
            "content": chunk.page_content,
            "embedding": vector,

            # Metadata
            "page": chunk.metadata.get("page"),
            "source": chunk.metadata.get("source"),
        }
    )

# -----------------------------
# Upsert
# -----------------------------
response = index.documents.upsert(
    namespace="default",
    documents=pinecone_docs,
)

print(response)

print("\n✅ Ingestion Completed")