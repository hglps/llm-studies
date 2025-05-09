from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ArticleUploadForm
from .models import Article
from .tasks import process_article_task, index_article_rag_task
from celery import chain


def home(request):
    return render(request, 'analyzer/home.html', {})

def upload_article(request):
    if request.method == 'POST':
        form = ArticleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.processing_status = 'pending'
            article.file_type = 'pdf'
            article.title = ''.join(article.uploaded_file.name.split('.')[:-1])
            # First save the article with filename, then process it
            # and change to actual article name
            article.save()
            
            (
                chain(
                    index_article_rag_task.s(article.id, chunk_size=500, overlap=100),
                    process_article_task.si(article.id),
                )()
            )
            
            return redirect(reverse('article_list'))
    else:
        form = ArticleUploadForm()
    return render(request, 'analyzer/upload.html', 
                  {'form': form})


def article_list(request):
    articles = Article.objects.order_by('-upload_date')
    return render(request, 'analyzer/article_list.html', 
                  {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    analysis = getattr(article, 'analyses', None)
    
    authors_list = []
    keywords_list = []
    if analysis:
        authors = analysis.authors or ""
        keywords = analysis.keywords or ""

        authors_list = [a.strip() for a in authors.split(';') if a.strip()]
        keywords_list = [k.strip() for k in keywords.split(';') if k.strip()]


    return render(request, 'analyzer/article_detail.html',
                  {'article': article,
                   'analysis': analysis,
                   'authors_list': authors_list,
                   'keywords_list': keywords_list})