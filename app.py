from flask import Flask, request, jsonify
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document  # Import Document class
from transformers import pipeline
import torch 
import pdfplumber 
import os

app = Flask(__name__)
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/multi-qa-mpnet-base-cos-v1",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)   
# Initialize a local text generation pipeline
generator = pipeline (
"text-generation",
model="facebook/bart-large",
device = 0 if torch.cuda.is_available() else -1 
)

# Directory to save uploaded files
UPLOAD_FOLDER = 'data'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ingest PDF and create FAISS index
@app.route('/ingest', methods=['POST'])
def ingest_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        with pdfplumber.open(file_path) as pdf:
            raw_texts = [page.extract_text() for page in pdf.pages if page.extract_text()]
        # Convert raw text to Document objects
        documents = [Document(page_content=text) for text in raw_texts]
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local("embeddings/index")
        return jsonify({"status": "success", "file_path": file_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Query the FAISS index
@app.route('/query', methods=['POST'])
def query_pdf():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    try:
        # vectorstore = FAISS.load_local("embeddings/index", embeddings)
        vectorstore = FAISS.load_local("embeddings/index", embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        results = retriever.get_relevant_documents(query)
        contents = [doc.page_content for doc in results]
        
        #create a prompt for natural response
        # prompt = f"As a friendly and knowledgeable assistant, based on the information extracted from a PDF provided in this context: {' '.join(contents)}, provide a clear, engaging, and concise answer to the query: {query}. Summarize relevant details from the PDF and keep the response natural and helpful."
        
        # Refined prompt to generate only the answer
        prompt = f"Context from PDF: {' '.join(contents)}\n\nBased on this context, provide a clear, engaging, and concise answer to the query: {query}. Summarize relevant details and keep it natural and helpful."
        response = generator(prompt,max_new_tokens=100, num_return_sequences=1)[0]['generated_text']
        
        return jsonify({"results": response.capitalize() + " 😊 Let me know if you need more help!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)