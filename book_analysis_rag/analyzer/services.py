from django.conf import settings
import pymupdf
import os
import requests, json
import logging

logger = logging.getLogger(__name__)

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
        
    def filter_response(self, response) -> dict:
        response_text = response['candidates'][0]['content']['parts'][0]['text']
        try:
            removing_tag = response_text.strip().removeprefix("```json").removesuffix("```").strip()
            filtered_response = json.loads(removing_tag)
            return filtered_response
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON response")
            return {}


    def analyze(self, text: str) -> dict:

        prompt = f"""
        Context: {text}

        Task: Return ONLY in JSON with the following fields and types:
        -"title": str,
        -"year":  str,
        -"authors": list of str,
        -"summary": str,
        -"keywords": list of str,
        -"objectives": str,
        -"methodology": str,
        -"conclusions": str,
        -"suggested_field": str

        Consider the following:
        - The submitted text is a scientific article.
        - The title is the article's title and should be retrieved from the text.
        - The authors should be a list of authors' names described in the text.
        - The year should be the publication year of the article, if it is described in the text.
        - The summary should be a concise overview of the article, including the main findings and contributions.
        - The keywords should be relevant terms that capture the main topics of the article, including the keywords found in the abstract.
        - The objectives should describe the main goals of the research.
        - The methodology should outline the research methods used in the study and why they were used, if it is described.
        - The conclusions should summarize the main findings and their implications.
        - The suggested_field should be a field of study that the article is related to, if it is described.
        """

        headers = {
            'x-goog-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        # payload = {
        #     'prompt': prompt,
        #     'max_tokens': 800,
        # }
        
        payload = {
            'contents': [{
                'parts': [{
                    'text': prompt
                }]
            }]
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        # response = requests.post(self.api_url, data=prompt, headers=headers)
        response.raise_for_status()
        
        return self.filter_response(response.json())
