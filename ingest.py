import glob
import json
import os
import ollama
from pptx import Presentation

chunks = []

for path in glob.glob("slides/*.pptx"):
    deck_name = os.path.basename(path)
    prs = Presentation(path)

    for slide_number, slide in enumerate(prs.slides, start=1):
        texts = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                texts.append(shape.text_frame.text)

        slide_text = " ".join(texts).strip()

        if slide_text == "":
            continue

        chunks.append({
            "deck": deck_name,
            "slide": slide_number,
            "text": slide_text,
        })

print("Total chunks:", len(chunks))
print("Embedding slides... (this can take a minute)")
for chunk in chunks:
    result = ollama.embed(model="nomic-embed-text", input="search_document: " + chunk["text"])
    chunk["embedding"] = result["embeddings"][0]

with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f)

print("Saved", len(chunks), "cards to chunks.json")
