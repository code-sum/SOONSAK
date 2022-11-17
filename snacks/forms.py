from django import forms
from .models import Snack, snack_Category

class CategoryForm(forms.ModelForm):

    class Meta:
        model = snack_Category
        fields = [
            'category'
        ]

        labels = {
             'category': '카테고리',   
        }

class SnackForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=snack_Category.objects.all(),label="카테고리")

    class Meta:
        model = Snack
        fields = [
            'category',
            'name',
            'content',
            'snack_image',
            'price',
            'stock',
            ]
        
        labels = {
            'name': '이름',
            'content': '설명',
            'snack_image': '이미지',
            'price': '가격',
            'stock': '개수',
        }