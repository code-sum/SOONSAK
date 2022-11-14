from django import forms
from .models import Snack, snack_Category

class CategoryForm(forms.ModelForm):

    class Meta:
        model = snack_Category
        fields = [
            'category'
        ]


class SnackForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=snack_Category.objects.all())

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

