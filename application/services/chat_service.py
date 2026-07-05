from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(context_chunks, question):
    context = "\n\n".join(context_chunks)

    prompt = f"""
    You are a precise and reliable AI assistant.

    Follow these rules strictly:
    1. Answer ONLY using the provided context.
    2. Do NOT use prior knowledge or make assumptions.
    3. If the answer is not clearly present in the context, then reply dynamically according to your reasoning capabilities.
    4. Keep the answer concise and factual.
    5. **ALWAYS use Markdown formatting** for better readability:
        - **Bold** for headings/emphasis: **Important term**
        - *Italics* for definitions: *definition*
        - Bullet lists: - Item one\n- Item two
        - Numbered lists: 1. First\n2. Second
        - Tables: | Header | Value |\n|--------|-------|\n| Data   | 123   |
        - Code: `inline` or ```python\ncode\n```
    6. Do not explain beyond what is asked.
    7. Quote exact phrases with > or ".

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",  # ✅ fast + good for RAG
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    

    return response.choices[0].message.content