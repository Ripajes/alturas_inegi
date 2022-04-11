from django import forms
from django.db.models import fields
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('author', 'title','description', 'document','original_id')