from django.contrib import admin

from .models import Article, ArticleAnalysis

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "upload_date", "processing_status")
    list_filter = ("processing_status",)
    

@admin.register(ArticleAnalysis)
class ArticleAnalysisAdmin(admin.ModelAdmin):
    list_display = ("article", "analysis_timestamp")
