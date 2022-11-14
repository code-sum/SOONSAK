from django.db import models
from snacks.models import Snack
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Review(models.Model):
    # 리뷰할 상품
    snack = models.ForeignKey(Snack, on_delete=models.CASCADE, related_name="snack_review")
    # 리뷰 내용
    content = models.TextField()
    # 후기 사진
    review_image = ProcessedImageField(
        upload_to="images/reviews/",
        blank=True,
        processors=[ResizeToFill(300, 480)],
        format="JPEG",
        options={"quality": 100},
    )
    # 작성시간
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정시간
    updated_at = models.DateTimeField(auto_now=True)
    # 작성자
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    # 상품에 대한 별점
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)

class Comment(models.Model):
    # 댓글 내용
    content = models.CharField(max_length=100)
    # 댓글 작성시간
    created_at = models.DateTimeField(auto_now_add=True)
    # 댓글 작성자
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    # 리뷰에 대한 코멘트
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')