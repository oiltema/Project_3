from django import forms
from PIL import Image

from .models import Comments, Food, SubCategory, Category, StepFood
from taggit.models import Tag


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 1, 'cols': 50}),
        }


class FoodAddForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['subcategory', 'title', 'image', 'time_cook', 'portion', 'description', 'products']


class StepFoodAddForm(forms.ModelForm):
    class Meta:
        model = StepFood
        fields = ['image', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 35}),
        }