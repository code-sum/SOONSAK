from django import forms
from .models import Review, Comment
from .widgets import starWidget

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'content',
            'review_image',
            'grade',
        ]
    
        labels = {
            "grade": "별점을 남겨주세요",
        }
        widgets = {
            "grade": starWidget,
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]