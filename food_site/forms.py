from django import forms

from .models import Comments


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 1, 'cols': 50}),
        }