from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import json

from pinecone import Pinecone

from dotenv import load_dotenv
import os

load_dotenv()


# -----------------------------
# MarkDown Loader
# -----------------------------
loader = TextLoader("data/environment_policy.md", encoding="utf-8")
documents = loader.load()

# -----------------------------
# Load PDF
# -----------------------------
#loader = PyPDFLoader("data/environment_policy.pdf")
#loader = PyPDFLoader("data/hr_policy.pdf")
#loader = PyPDFLoader("data/safety_manual.pdf")
#documents = loader.load()

# -----------------------------
# Chunking
# -----------------------------
markdown_text = documents[0].page_content

headers_to_split_on = [
    ("#", "Document"),
    ("##", "Section"),
    ("###", "Subsection"),
]

header_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

header_docs = header_splitter.split_text(markdown_text)

# -------------- Adding source metadata to each chunk --------------
source = documents[0].metadata.get("source")

for doc in header_docs:
    doc.metadata["source"] = source

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)

chunks = recursive_splitter.split_documents(header_docs)

print(f"Total Chunks : {len(chunks)}")

# -----------------------------
# Embedding Model
# -----------------------------
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
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
bm25_corpus = []

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
            "document": chunk.metadata.get("Document"),
            "section": chunk.metadata.get("Section"),
            "subsection": chunk.metadata.get("Subsection"),
        }
    )

    bm25_corpus.append(
        {
            "id": f"chunk-{i}",
            "content": chunk.page_content,
            "metadata": {
                "page": chunk.metadata.get("page"),
                "source": chunk.metadata.get("source"),
                "document": chunk.metadata.get("Document"),
                "section": chunk.metadata.get("Section"),
                "subsection": chunk.metadata.get("Subsection"),
            }
        }
    )


# -----------------------------
# Upsert into Pinecone
# -----------------------------
response = index.documents.upsert(
    namespace="default",
    documents=pinecone_docs,
)


# -----------------------------
# Create BM25 Corpus JSON
# -----------------------------
with open("data/bm25_corpus.json", "w", encoding="utf-8") as file:
    json.dump(
        bm25_corpus,
        file,
        indent=4,
        ensure_ascii=False
    )

print(response)

print("\n✅ Ingestion Completed")