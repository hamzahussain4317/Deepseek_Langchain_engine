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
    full_text = "\n".join(
        page.extract_text() for page in reader.pages if page.extract_text()
    )
    documents = []
    #Extract Acronym section
    acronyms_match=re.search(r"ACRONYMS\s*\n(.*?)(?=\n*DEFINITIONS\s*\n)",full_text,re.DOTALL|re.IGNORECASE)
    if acronyms_match:
        acronym_text=acronyms_match.group(0).strip()
        documents.append(Document(
            page_content=acronym_text,
            metadata={"section":"Acronyms","Chunk_id":0}
        ))
    #Extract definition Section
    definition_match=re.search(r"DEFINITIONS\s*\n(.*?)(?=\n*REGULATION\s*[-–]?\s*\d+\s*\n)",full_text,re.DOTALL|re.IGNORECASE)  
    if definition_match:
        definition_text="DEFINITIONS\n"+definition_match.group(1).strip()
        documents.append(Document(
            page_content=definition_text,
            metadata={"section":"Definitions","chink_id":1}
        ))  
        

    #make a seperate chunk for each regulation
    pattern = re.compile(
        r"(REGULATION\s*[-–]?\s*(\d+)\s*\n([^\n]+)\n)(.*?)(?=(REGULATION\s*[-–]?\s*\d+\s*\n|$))",
        re.DOTALL,
    )
    

    for idx, match in enumerate(pattern.findall(full_text), start=2):
    # for match in pattern.findall(full_text):
        header, reg_number, title, body = match[:4]
        full_content = f"{header}{body}".strip()

        doc = Document(
            page_content=full_content,
            metadata={
                "regulation_number": str(reg_number),
                "title": title.strip(),
                "chunk_id": idx,
            },
        )
        documents.append(doc)

    return documents
