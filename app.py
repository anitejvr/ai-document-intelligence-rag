from flask import Flask, render_template, request, session
from openai import OpenAI
from dotenv import load_dotenv
import os
import PyPDF2
import faiss
import numpy as np

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory stores for now
vector_index = None
document_chunks = []


def extract_pdf_text(pdf_file):
    pdf_text = ""
    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text + "\n"

    return pdf_text


def chunk_text(text, chunk_size=1200, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def create_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def build_vector_store(chunks):
    embeddings = []

    for chunk in chunks:
        embedding = create_embedding(chunk)
        embeddings.append(embedding)

    embeddings_array = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings_array.shape[1])
    index.add(embeddings_array)

    return index


def search_relevant_chunks(question, top_k=3):
    global vector_index
    global document_chunks

    question_embedding = create_embedding(question)
    question_vector = np.array([question_embedding]).astype("float32")

    distances, indices = vector_index.search(question_vector, top_k)

    relevant_chunks = []

    for i in indices[0]:
        relevant_chunks.append(document_chunks[i])

    return relevant_chunks


def generate_document_insights(pdf_text):
    prompt = f"""
    Analyze this document and provide:

    Executive Summary

    Key Findings (5 bullet points)

    Risks or Concerns

    Recommended Actions

    Document:

    {pdf_text}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def answer_question_with_rag(question):
    relevant_chunks = search_relevant_chunks(question)

    context = "\n\n---\n\n".join(relevant_chunks)

    prompt = f"""
    You are a document intelligence assistant.

    Answer the user's question using ONLY the relevant document excerpts below.

    If the answer cannot be found in the excerpts, respond:
    "The document does not contain enough information to answer that question."

    Relevant Document Excerpts:

    {context}

    Question:

    {question}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def index():
    global vector_index
    global document_chunks

    answer = None
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "upload":
            pdf_file = request.files.get("pdf_file")

            if not pdf_file:
                error = "Please upload a PDF."
            else:
                pdf_text = extract_pdf_text(pdf_file)

                if not pdf_text.strip():
                    error = "Could not extract readable text from this PDF."
                else:
                    session["pdf_loaded"] = True

                    document_chunks = chunk_text(pdf_text)
                    vector_index = build_vector_store(document_chunks)

                    document_insights = generate_document_insights(pdf_text)
                    session["document_insights"] = document_insights

        elif action == "question":
            question = request.form.get("question", "").strip()

            if not question:
                answer = "Please enter a question."
            elif vector_index is None or not document_chunks:
                answer = "Please upload and analyze a document first."
            else:
                answer = answer_question_with_rag(question)

    uploaded = session.get("pdf_loaded") is True

    return render_template(
        "index.html",
        answer=answer,
        error=error,
        uploaded=uploaded,
        document_insights=session.get("document_insights")
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )