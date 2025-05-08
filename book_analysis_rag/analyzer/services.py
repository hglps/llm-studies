from django.conf import settings
import pymupdf
import os
import requests, json

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
        with pymupdf.open(file_path) as doc:
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


class GeminiClient:
    def __init__(self):
        self.api_url = settings.GEMINI_API_URL
        self.api_key = settings.GEMINI_API_KEY

    def analyze(self, text: str) -> dict:

        prompt = f"""
        Context: {text}

        Task: Return ONLY in JSON with the following fields:
        {
            "summary": "...",
            "keywords": [...],
            "objectives": "...",
            "methodology": "...",
            "conclusions": "...",
            "suggested_field": "..."
        }
        """
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        # payload = {
        #     'prompt': prompt,
        #     'max_tokens': 800,
        # }
        # response = requests.post(self.api_url, json=payload, headers=headers)
        response = requests.post(self.api_url, data=prompt, headers=headers)
        response.raise_for_status()
        return response.json()
