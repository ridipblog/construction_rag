import fitz  # PyMuPDF
import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def chunk_text(text: str, chunk_size: int = 700, chunk_overlap: int = 100) -> List[str]:
    """
    Splits document text into overlapping semantic chunks for vector retrieval.
    """
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return []

    words = text.split(' ')
    chunks = []
    current_words = []
    current_length = 0

    for word in words:
        current_words.append(word)
        current_length += len(word) + 1
        if current_length >= chunk_size:
            chunk = " ".join(current_words)
            chunks.append(chunk)
            overlap_words = current_words[-int(len(current_words) * (chunk_overlap / chunk_size)):]
            current_words = list(overlap_words)
            current_length = sum(len(w) + 1 for w in current_words)

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks

def extract_and_chunk_pdf(file_bytes: bytes, filename: str) -> List[Dict[str, Any]]:
    """
    Extracts text from PDF bytes and produces chunked documents with page metadata.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    all_chunks = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        if not text.strip():
            continue

        page_chunks = chunk_text(text)
        for i, chunk in enumerate(page_chunks):
            all_chunks.append({
                "content": chunk,
                "source": f"{filename} (Page {page_num + 1})",
                "metadata": {
                    "filename": filename,
                    "page": page_num + 1,
                    "chunk_index": i + 1,
                    "total_pages": len(doc)
                }
            })

    logger.info(f"Extracted {len(all_chunks)} chunks from {filename} ({len(doc)} pages)")
    return all_chunks

