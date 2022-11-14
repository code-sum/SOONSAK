from django.db import models
# moon models
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.contrib.auth import get_user_model
from django.urls import reverse

# AUTH_USER_MODEL User로 가져오기
User = get_user_model()

class snack_Category(models.Model):
    category = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.category
    def get_absolute_url(self):
        #카테고리를 선택하면 해당 url로 넘어감, 수정필요 넘어갈 페이지 재검토
        return reverse('snacks:index', args=[self.category]) 

# Snacks => Snack 변경
class Snack(models.Model):
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
    # settings.AUTH_USER_MODEL => User로 변경
    likes=models.ManyToManyField(User ,related_name="likes")
    # 가격
    price=models.PositiveIntegerField()
    # 재고
    stock=models.PositiveIntegerField()

    def __str__(self):
        return self.name   