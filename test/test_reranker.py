from sentence_transformers import CrossEncoder

print("Loading Cross Encoder...")

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

print("Model Loaded Successfully!")

query = "What is OOP in Python?"

chunks = [
    "Python is a high-level programming language.",
    "List is mutable and Tuple is immutable.",
    "Classes, Objects, Inheritance and Polymorphism are core OOP concepts.",
]

pairs = [(query, chunk) for chunk in chunks]

scores = model.predict(pairs)

print("\nScores:\n")

for chunk, score in zip(chunks, scores):
    print(f"{score:.4f}  -->  {chunk}")


'''
Model Loaded Successfully!

Scores:

-0.3480  -->  Python is a high-level programming language.
-10.1086  -->  List is mutable and Tuple is immutable.
0.5847  -->  Classes, Objects, Inheritance and Polymorphism are core OOP concepts.
'''