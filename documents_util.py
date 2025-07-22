# from langchain_community.document_loaders import PyPDFLoader
# from langchain.schema import Document
# import re
# def load_pdf(path:str):
#     loader=PyPDFLoader(path)
#     pages=loader.load()
    
#     full_text="\n".join([p.page_content for p in pages])
    
#     pattern=re.compile(r"(REGULATION\s*[-–]?\s*(\d+)\s*\n([^\n]+)\n)(.*?)(?=(REGULATION\s*[-–]?\s*\d+\s*\n|$))", re.DOTALL)
#     matches=pattern.findall(full_text)
#     documents=[]
    
#     for idx,(header,reg_num,reg_title,content,_) in enumerate(matches):
#         page_content=f"{header}{content}".strip()
#         metadata={
#             "regulation_number":reg_num.strip(),
#             "title":reg_title.strip(),
#             "chunk_id":idx
#         }
#         documents.append(Document(page_content=page_content,metadata=metadata))
        
#         return documents

import re
from PyPDF2 import PdfReader
from langchain.schema import Document

def load_pdf(path: str) -> list[Document]:
    reader = PdfReader(path)
    full_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

    pattern = re.compile(
        r"(REGULATION\s*[-–]?\s*(\d+)\s*\n([^\n]+)\n)(.*?)(?=(REGULATION\s*[-–]?\s*\d+\s*\n|$))",
        re.DOTALL
    )

    documents = []
    for match in pattern.findall(full_text):
        header, reg_number, title, body = match[:4]
        full_content = f"{header}{body}".strip()

        doc = Document(
            page_content=full_content,
            metadata={
                "regulation_number": str(reg_number),
                "title": title.strip(),
                "chunk_id": 0
            }
        )
        documents.append(doc)

    return documents
