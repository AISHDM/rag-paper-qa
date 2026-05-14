from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()

def load_rag_pipeline(db_dir="chroma_db"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma(
        persist_directory=db_dir,
        embedding_function=embeddings
    )
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    prompt = ChatPromptTemplate.from_template("""
You are a research assistant. Answer the question using ONLY 
the context provided from the research papers. If the answer 
isn't in the context, say "I couldn't find that in the papers."

Context:
{context}

Question: {question}

Answer:""")
    
    return vectorstore, llm, prompt

def ask(question, vectorstore, llm, prompt, k=4):
    # Step 1: Retrieve top-k relevant chunks
    docs = vectorstore.similarity_search(question, k=k)
    context = "\n\n".join([d.page_content for d in docs])
    
    # Step 2: Generate answer
    chain = prompt | llm
    response = chain.invoke({
        "context": context,
        "question": question
    })
    
    return {
        "question": question,
        "answer": response.content,
        "sources": [d.metadata.get("source", "unknown") for d in docs]
    }

if __name__ == "__main__":
    print("Loading RAG pipeline...")
    vectorstore, llm, prompt = load_rag_pipeline()
    
    questions = [
        "What is the attention mechanism?",
        "How does message passing work in GNNs?",
        "What datasets were used in the transformer paper?"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        result = ask(q, vectorstore, llm, prompt)
        print(f"A: {result['answer']}")
        print(f"Sources: {set(result['sources'])}")
        print("-" * 60)