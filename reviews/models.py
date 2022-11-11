from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from accounts.models import User

# Create your models here.
class Review(models.Model):
    content = models.TextField()
    review_image = ProcessedImageField(
        upload_to="images/reviews/",
        blank=True,
        processors=[ResizeToFill(300, 480)],
        format="JPEG",
        options={"quality": 100},
    )
    # stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')

class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')