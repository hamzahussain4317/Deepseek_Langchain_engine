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



# import os
# import re
# from typing import List
# from PyPDF2 import PdfReader
# from langchain.schema import Document
# from llm_client import ask_deepseek  # LLM agent using DeepSeek

# # ------------------------
# # Step 1: Extract plain text from a single PDF
# # ------------------------
# def extract_text_from_pdf(path: str) -> str:
#     reader = PdfReader(path)
#     return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])


# # ------------------------
# # Step 2: Prepare text for all PDFs for LLM chunking
# # ------------------------
# def prepare_files_for_llm(pdf_paths: List[str]) -> str:
#     """
#     Extracts and wraps all PDFs with identifiable <<FILE:...>> and <<END_OF_FILE>> tags
#     """
#     full_text = ""
#     for path in pdf_paths:
#         filename = os.path.basename(path)
#         text = extract_text_from_pdf(path)
#         # Mark file boundaries so we can track which chunk belongs to which file
#         full_text += f"\n<<FILE:{filename}>>\n{text.strip()}\n<<END_OF_FILE>>\n"
#     return full_text


# # ------------------------
# # Step 3: Ask LLM to insert <<<BREAK>>> markers for clean semantic chunking
# # ------------------------
# def insert_breakpoints_with_llm(document_text: str) -> str:
#     prompt = f"""
# You are a document chunking assistant.

# Your task:
# - Split regulation/guideline documents into meaningful and logically separate chunks.
# - Insert <<<BREAK>>> before each new section, point, regulation, or topic.
# - Keep all content intact.
# - Do NOT break inside a sentence or bullet point.
# - Files are wrapped like <<FILE:filename.pdf>> ... <<END_OF_FILE>>

# Here is the full text:
# {document_text}
#     """
#     return ask_deepseek(prompt)


# # ------------------------
# # Step 4: Parse the LLM output and extract metadata (filename, regulation number, etc.)
# # ------------------------
# def parse_llm_chunks(llm_output: str) -> List[Document]:
#     docs = []
#     current_file = "unknown"
#     chunks = llm_output.split("<<<BREAK>>>")

#     for idx, chunk in enumerate(chunks):
#         chunk = chunk.strip()
#         if not chunk:
#             continue

#         # Update current filename when we hit a new file tag
#         file_match = re.search(r"<<FILE:(.*?)>>", chunk)
#         if file_match:
#             current_file = file_match.group(1).strip()

#         # Clean out <<FILE:...>> and <<END_OF_FILE>> from chunk content
#         chunk_clean = re.sub(r"<<.*?>>", "", chunk).strip()

#         # Extract metadata based on content patterns
#         reg_match = re.search(r"REGULATION\s*[-–]?\s*(\d+)", chunk, re.IGNORECASE)
#         point_match = re.search(r"^\s*(\d+)[.)]\s", chunk)  # e.g., 1) or 1.

#         metadata = {
#             "filename": current_file,
#             "chunk_id": idx
#         }

#         if reg_match:
#             metadata["regulation_number"] = reg_match.group(1)
#         elif point_match:
#             metadata["point_number"] = point_match.group(1)

#         docs.append(Document(page_content=chunk_clean, metadata=metadata))

#     return docs


# # ------------------------
# # 🔄 FINAL FUNCTION: Load & Chunk All PDFs with LLM
# # ------------------------
# def load_all_pdfs_with_llm(pdf_paths: List[str]) -> List[Document]:
#     print("🔄 Extracting and preparing text from all PDFs...")
#     joined_text = prepare_files_for_llm(pdf_paths)

#     print("🧠 Asking LLM to insert breakpoints...")
#     llm_output = insert_breakpoints_with_llm(joined_text)

#     print("📦 Parsing LLM output into chunks with metadata...")
#     return parse_llm_chunks(llm_output)
