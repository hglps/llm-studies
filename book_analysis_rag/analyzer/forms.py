from django import forms
from .models import Article

class ArticleUploadForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['uploaded_file']
        
    def clean_uploaded_file(self):
        file = self.cleaned_data.get('uploaded_file')
        
        valid_exts = ['.pdf', '.txt']
        ext = file.name.lower().split('.')[-1]
        
        if f".{ext}" not in valid_exts:
            raise forms.ValidationError("Unsupported file type. Please upload a PDF or TXT file.")
        
        max_mb_size = 25
        
        if file.size > max_mb_size * 1024 * 1024:
            raise forms.ValidationError(f"File size exceeds {max_mb_size}MB limit.")
        return file
