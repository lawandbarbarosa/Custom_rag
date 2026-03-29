# 📚 Simko Custom RAG System

An AI-powered Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents, index them into a vector database, and ask questions grounded in those documents.

the webpage: https://customrag-gswe3973hjvylmyissk7us.streamlit.app/

---

## 🚀 Overview

Simko Custom RAG is a backend-first application that combines:

* 📄 **Document ingestion (PDFs)**
* 🧠 **Semantic search with Pinecone**
* 🤖 **LLM-powered answers using OpenAI**
* ⚡ **FastAPI for API access**

The system enables users to:

* Upload documents
* Automatically process and embed them
* Ask natural language questions
* Receive context-aware answers grounded in their data

---

## 🧠 How It Works

### Step 1: Upload Documents

* Users upload PDF files via API
* Files are temporarily stored and processed
* Documents are split into chunks for better retrieval

### Step 2: Embedding & Indexing

* Text chunks are converted into vector embeddings using OpenAI
* Stored in a Pinecone vector database

### Step 3: Querying

* User submits a question
* System retrieves the most relevant chunks
* LLM generates an answer using retrieved context

---

## 🏗️ Project Structure

```id="ragstruct01"
.
├── main.py        # Core RAG logic (loading, splitting, querying)
├── app.py         # FastAPI server (upload + query endpoints)
├── temp_uploads/  # Temporary storage for uploaded files
└── README.md
```

---

## ⚙️ Requirements

* Python 3.9+
* OpenAI API Key
* Pinecone API Key

---

## 🔐 Environment Variables

Create a `.env` file:

```id="ragenv01"
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
```

---

## ▶️ Running the Application

Start the FastAPI server:

```id="ragrun01"
uvicorn app:app --reload --port 8001
```

Server will be available at:

```id="ragurl01"
http://127.0.0.1:8001
```

---

## 📡 API Endpoints

---

### 🔹 1. Upload PDF

```id="ragupload01"
POST /upload
```

#### Description

Uploads a PDF, processes it, and indexes it into Pinecone.

#### Request

* Form-data:

  * `file`: PDF file

#### Response

```json id="ragupload02"
{
  "messages": "Successfully indexed file.pdf",
  "chunks": 42
}
```

---

### 🔹 2. Ask a Question

```id="ragask01"
POST /ask
```

#### Request Body

```json id="ragask02"
{
  "prompt": "What is the main topic of the document?"
}
```

#### Response

```json id="ragask03"
{
  "answer": "The document discusses..."
}
```

---

### 🔹 3. Health Check

```id="raghealth01"
GET /health
```

#### Response

```json id="raghealth02"
{
  "status": "healthy"
}
```

---

## 🧩 Core Components

### 📄 Document Loader

* Uses `PyPDFLoader` to extract text from PDFs 

### ✂️ Text Splitting

* Recursive chunking for optimal retrieval
* Handles large documents efficiently 

### 🧠 Embeddings

* OpenAI embeddings (`text-embedding-3-small`)
* Converts text into vector representations

### 🗂️ Vector Store

* Pinecone for scalable similarity search
* Stores and retrieves document chunks 

### 🤖 LLM Query Engine

* Retrieves top-k relevant chunks
* Uses GPT model to generate answers
* Ensures answers are grounded in context 

---

## 🎯 Features

* ✅ PDF document ingestion
* ✅ Automatic chunking & embedding
* ✅ Pinecone vector database integration
* ✅ Context-aware Q&A
* ✅ FastAPI-based architecture
* ✅ Scalable and modular design

---

## ⚠️ Important Notes

* Only **PDF files** are supported for upload
* Uploaded files are **temporarily stored and deleted after processing** 
* Answers depend on the **quality and content of uploaded documents**
* If no relevant context is found, the system returns:

  > "I don't know."

---

## 🔮 Future Improvements

* 🌐 Web UI (Streamlit or React frontend)
* 📊 Document management dashboard
* 🔍 Hybrid search (keyword + vector)
* 🧾 Support for multiple file types (DOCX, TXT)
* 🗄️ Persistent document storage
* 🔐 Authentication & user sessions

---

## 🧑‍💻 Tech Stack

* Python
* FastAPI
* LangChain
* OpenAI API
* Pinecone
* PyPDF

---

## 📬 Contributing

Contributions are welcome!

* Open issues for bugs or improvements
* Submit pull requests with enhancements

---

## 📄 License

MIT License

---

## 💡 Author

Built as part of the Simko AI Systems 🚀
