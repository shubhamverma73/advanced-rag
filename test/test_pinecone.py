from pinecone import Pinecone
import pinecone

print("Version:", pinecone.__version__)

pc = Pinecone(api_key="dummy")

print("Has indexes:", hasattr(pc, "indexes"))

print("\nMethods:")
print([x for x in dir(pc) if not x.startswith("_")])