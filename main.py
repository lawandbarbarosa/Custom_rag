import os
from langchain_community.document_loaders import PyPDFLoader

def load_documents(folder_path: str):
    # 1. Check if the path exists AND if it is actually a directory
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"The directory: {folder_path} does not exist.")

    documents = []
    
    # 2. Iterate through files
    for filename in os.listdir(folder_path):
        # Filter for PDF files and ignore hidden system files
        if filename.endswith(".pdf") and not filename.startswith("._"):
            file_path = os.path.join(folder_path, filename)
            print(f"📄 Loading: {filename}")
            
            try:
                loader = PyPDFLoader(file_path)
                # .load() returns a list of Document objects (one per page)
                documents.extend(loader.load())
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")
                
    return documents

from dotenv import load_dotenv
load_dotenv()
import os
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 400
    )
    chunks = splitter.split_documents(documents)
    print(f"✂️ Created {len(chunks)} chunks")
    return chunks

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

from pinecone import Pinecone

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("simkoyragy")


from langchain_pinecone import PineconeVectorStore


def create_vector_database(chunks):
    vector_store = PineconeVectorStore.from_documents(
        document=chunks,
        embedding=embeddings,
        index_name= "simkoyragy",
    )
    return vector_store


from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1200,
        chunk_overlap = 200
    )
    chunks = splitter.split_documents(documents)
    print(f"✂️ Created {len(chunks)} chunks")
    return chunks


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser



def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


os.environ["PINECONE_API_KEY"] = "pcsk_58St2a_JCKMGaZe19qVEGQsP3VDBW5X2m8X5XN2MsMxagpoXguQYEaKRaw6oJhcLRJRVo1"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def query_rag_system(query_text, vector_store):
    llm = ChatOpenAI(model="gpt-5.2", temperature=0, api_key=openai_api_key) # Make sure you have Ollama installed and running!

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful assistant. Use the provided context to answer the question. 
        The context may contain formatting or spacing issues; please interpret it reasonably.
        If the context definitely does not contain the answer, say "I don't know."

        Context:
        {context}

        Question:
        {question}
        """
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(query_text)

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os


def main():
    # 1. Initialize Embeddings (Crucial missing piece)
    
    # 2. Connect to the index correctly
    # We use the class constructor to connect, not .from_documents
    vector_store = PineconeVectorStore(index_name='simkoyragy', embedding=embeddings)

    # 3. Check if empty using the official client
    index_stats = pc.Index('simkoyragy').describe_index_stats()
    
    if index_stats["total_vector_count"] == 0:
        print("📦 Pinecone index empty. Processing documents...")
        
        # Ensure these functions are defined or imported!
        docs = load_documents(".") 
        chunks = split_text(docs)

        # Now we use from_documents to actually upload
        vector_store = PineconeVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            index_name='simkoyragy',
            api_key=pinecone_api_key
        )
        print("Vector database created")

    while True:
        query = input("\n ❓ Ask a question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        print("🤔 Thinking...")
        answer = query_rag_system(query, vector_store)
        print("\n🧠 Answer:")
        import textwrap
        print(textwrap.fill(answer, width=80))


if __name__ == "__main__":
    main()