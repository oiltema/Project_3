from django import forms

from .models import Category, SubCategory, Performer, MyWork, TypeWork, Review


class PerformerCreateForm(forms.ModelForm):
    class Meta:
        model = Performer
        fields = ['category', 'city', 'phone', 'description']


class MyWorkAddForm(forms.ModelForm):
    class Meta:
        model = MyWork
        fields = ['image', 'title', 'description', 'price']
        widgets = {'description': forms.Textarea(attrs={'rows': 2, 'cols': 40})}


class TypeWorkAddForm(forms.ModelForm):
    class Meta:
        model = TypeWork
        fields = ['title', 'price']


class ReviewAddForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {'text': forms.TextInput(attrs={'size': '40'})}

