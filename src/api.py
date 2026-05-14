from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from rag import load_rag_pipeline, ask
import warnings
warnings.filterwarnings("ignore")

# Store pipeline in app state
pipeline = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading RAG pipeline...")
    vectorstore, llm, prompt = load_rag_pipeline()
    pipeline["vectorstore"] = vectorstore
    pipeline["llm"] = llm
    pipeline["prompt"] = prompt
    print("Ready.")
    yield
    pipeline.clear()

app = FastAPI(
    title="Research Paper Q&A",
    description="Ask questions about ML research papers using RAG",
    version="1.0.0",
    lifespan=lifespan
)

class Question(BaseModel):
    question: str
    k: int = 4  # number of chunks to retrieve

class Answer(BaseModel):
    question: str
    answer: str
    sources: list[str]

@app.get("/")
def root():
    return {"message": "Research Paper Q&A API", "status": "running"}

@app.post("/ask", response_model=Answer)
def ask_question(body: Question):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    result = ask(
        body.question,
        pipeline["vectorstore"],
        pipeline["llm"],
        pipeline["prompt"],
        k=body.k
    )
    return result

@app.get("/papers")
def list_papers():
    import glob
    papers = [p.split("/")[-1] for p in glob.glob("papers/*.pdf")]
    return {"papers": papers, "count": len(papers)}