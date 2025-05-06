import fitz
import os

class TextExtractor:
    @staticmethod
    def extract(file_path):
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == ".pdf":
            return TextExtractor._extract_pdf(file_path)
        else:
            raise ValueError("Formato de arquivo não suportado.")

    @staticmethod
    def _extract_pdf(file_path):
        text = []
        with fitz.open(file_path) as doc:
            for i, page in enumerate(doc):
                text.append(page.get_text())
        return "\n".join(text)


def chunk_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []
    i = 0
    
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks