import json

import numpy as np
import ollama

# 1. Load the cards
with open("chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 2. RETRIEVE: search.py packed into a function
def retrieve(question, k=3):
    result = ollama.embed(model="nomic-embed-text", input="search_query: " + question)
    question_vector = result["embeddings"][0]
    for chunk in chunks:
        chunk["score"] = cosine(question_vector, chunk["embedding"])
    return sorted(chunks, key=lambda c: c["score"], reverse=True)[:k]

question = input("Ask a question: ")
top3 = retrieve(question)

# 3. Staple the 3 slides into one block of text
context = ""
for c in top3:
    context += f'[{c["deck"]}, slide {c["slide"]}]\n{c["text"]}\n\n'

# 4. The exam rules for the AI
prompt = f"""You are a study assistant. Answer the question using ONLY the slides below.
After each fact, cite the slide like [deck, slide N].
If the slides don't contain the answer, say "I can't find that in your slides."

SLIDES:
{context}
QUESTION: {question}"""

# 5. GENERATE: the AI writes the answer
print("Thinking... (can take up to a minute)")
reply = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
print("\n" + reply["message"]["content"])

# 6. Show which slides were used
print("\nSources used:")
for c in top3:
    print(f'  {c["score"]:.3f}  {c["deck"]}, slide {c["slide"]}')