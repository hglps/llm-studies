from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='articles/')
    file_type = models.CharField(max_length=30, choices=[
        ('pdf', 'PDF'),
    ])
    upload_date = models.DateTimeField(auto_now_add=True)
    processing_status = models.CharField(max_length=50, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    ])
    extracted_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    

class ArticleAnalysis(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='analyses')
    year = models.CharField(max_length=4, blank=True, null=True)
    authors = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    methodology = models.TextField(blank=True, null=True)
    conclusions = models.TextField(blank=True, null=True)
    suggested_field = models.CharField(blank=True, null=True)    
    analysis_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis of {self.article.title}"
    
