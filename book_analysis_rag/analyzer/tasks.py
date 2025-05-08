from celery import shared_task
from .models import Article, ArticleAnalysis
from .services import TextExtractor, chunk_text, GeminiClient
from .vector_store import EmbeddingService, ChromaClient

@shared_task
def process_article_task(article_id):
    article = Article.objects.get(id=article_id)
    article.processing_status = 'processing'
    article.save()

    text = TextExtractor.extract(article.uploaded_file.path)
    article.extracted_text = text
    article.save()

    model = GeminiClient()
    result = model.analyze(text)
    # returns:
    # Dict: {summary, keywords, objectives, methodology, conclusions, suggested_field}

    ArticleAnalysis.objects.update_or_create(
        article=article,
        defaults={
            'summary':        result['summary'],
            'keywords':       ','.join(result.get('keywords', [])),
            'objectives':     result['objectives'],
            'methodology':    result['methodology'],
            'conclusions':    result['conclusions'],
            'suggested_field': result['suggested_field'],
        }
    )

    article.processing_status = 'completed'
    article.save()


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
