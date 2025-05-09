from celery import shared_task
from .models import Article, ArticleAnalysis
from .services import TextExtractor, chunk_text, GeminiClient
from .vector_store import EmbeddingService, ChromaClient


@shared_task
def process_article_task(article_id) -> dict:
    article = Article.objects.get(id=article_id)
    article.processing_status = 'processing'
    article.save()

    model = GeminiClient()
    result = model.analyze(article.extracted_text)
    # returns:
    # Dict: {title, year, authors, summary, keywords,
    #        objectives, methodology, conclusions,
    #        suggested_field}
        
    new_title = result.get('title')
    if new_title:
        # Update the article title in the db,
        # since the initial title is the filename
        article.title = new_title
        article.save(update_fields=['title'])

    ArticleAnalysis.objects.update_or_create(
        article=article,
        defaults={
            "year": result.get('year', ''),
            "authors": ";".join(result.get('authors', [])),
            "summary": result.get('summary', ''),
            "keywords": ";".join(result.get('keywords', [])),
            "objectives": result.get('objectives', ''),
            "methodology": result.get('methodology', ''),
            "conclusions": result.get('conclusions', ''),
            "suggested_field": result.get('suggested_field', ''),
        }
    )

    article.processing_status = 'completed'
    article.save()
    
    return result


@shared_task
def index_article_rag_task(article_id, chunk_size=500, overlap=100):
    article = Article.objects.get(id=article_id)

    text = article.extracted_text or TextExtractor.extract(article.uploaded_file.path)
    if not article.extracted_text:
        article.extracted_text = text
        article.save()

    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

    embedder = EmbeddingService()
    embeddings = embedder.embed(chunks)

    chroma = ChromaClient()
    chroma.add_chunks(article_id, chunks, embeddings)

    article.processing_status = 'pending'
    article.save()

    return article.id
