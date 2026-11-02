import json
import numpy as np
import ollama

# Load the index cards (with their embeddings)
with open("chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

# Score how similar two vectors are (1 = same meaning, 0 = unrelated)
def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Turn the question into its 768 numbers too
question = input("Ask a question: ")
result = ollama.embed(model="nomic-embed-text", input="search_query: " + question)
question_vector = result["embeddings"][0]

# Score every slide against the question
for chunk in chunks:
    chunk["score"] = cosine(question_vector, chunk["embedding"])

# Sort highest score first, keep the top 3
top3 = sorted(chunks, key=lambda c: c["score"], reverse=True)[:3]

for c in top3:
    print(f'{c["score"]:.3f}  [{c["deck"]}, slide {c["slide"]}]  {c["text"][:80]}')