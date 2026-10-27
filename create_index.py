from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

# Agar pehle se index hai to delete kar do
if pc.indexes.exists("simple-rag-md"):
    pc.indexes.delete("simple-rag-md")

index = pc.indexes.create(
    name="simple-rag-md",
    schema={
        "fields": {
            "content": {
                "type": "string",
                "full_text_search": {
                    "language": "en"
                }
            },
            "embedding": {
                "type": "dense_vector",
                "dimension": 3072,
                "metric": "cosine"
            }
        }
    },
    deployment={
        "deployment_type": "managed",
        "cloud": "aws",
        "region": "us-east-1"
    }
)

print(index)
print("✅ Index Created Successfully")


'''
MysQL vs Pinecone Comparison:

--------------------------------------
| MySQL         |           Pinecone |
|---------------|--------------------|
| Database      |           Index    |
| Table         |           Namespace|
| Row           |           Vector   |
--------------------------------------
'''