from django.db import models
# Create your models here.
# moon models
from django import forms
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.conf import settings
from django.urls import reverse



class snack_Category(models.Model):
    category = models.CharField(max_length=20, unique=True),
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        #카테고리를 선택하면 해당 url로 넘어감, 수정필요 넘어갈 페이지 재검토
        return reverse('snacks:index', args=[self.category]) 


class Snacks(models.Model):
    name=models.CharField(max_length=20)
    content=models.TextField(max_length=200)
    category=models.ForeignKey(snack_Category,max_length=50, blank=True, on_delete=models.CASCADE)
    snack_image= ProcessedImageField(
        upload_to="images/snacks/",
        blank=True,
        #이미지 사이즈 추후 조정
        processors=[ResizeToFill(300, 300)],
        #이미지 품질
        options={'quality': 80},
        format="JPEG",
    )
    # like=models.ManayToManyField(settings.AUTH_USER_MODEL,related_name="likes")
    price=models.IntegerField(blank=True)
    #장바구니 재고 재검토 필요
    stock=models.IntegerField(blank=True)


    