from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ArticleUploadForm
from .models import Article
from .tasks import process_article_task, index_article_rag_task


def home(request):
    return render(request, 'analyzer/home.html', {})

def upload_article(request):
    if request.method == 'POST':
        form = ArticleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.processing_status = 'pending'
            article.save()
            
            process_article_task.delay(article.id)
            index_article_rag_task.delay(article.id, chunk_size=500, overlap=100)
            
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
    article = Article.objects.get(id=article_id)
    return render(request, 'analyzer/article_detail.html', 
                  {'article': article})