from fastapi import FastAPI , UploadFile , File
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import ask_llm
from documents_util import load_pdf
from chroma_utils import add_docs_to_chroma , setup_bm25_retriever


app =FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#upload file endpoint
@app.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    with open("temp.pdf","wb") as f:
        f.write(await file.read())
    docs=load_pdf("temp.pdf")
    add_docs_to_chroma(docs)
    setup_bm25_retriever(docs)
    return {"message":"Document processed and added to Vector DB"}

#user QA endpoint
@app.post("/ask")
async def ask(query: str):
    result=ask_llm(query)
    return {"response": result['result']}
