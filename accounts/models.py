from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class User(AbstractUser):

    pass
    # 회원가입 주소
    address = models.CharField(max_length=250)
    # 팔로윙
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    # 프로필_이미지
    profile_image = ProcessedImageField(
        upload_to="images/accounts/",
        blank=True,
        processors=[ResizeToFill(300, 480)],
        format="JPEG",
        options={"quality": 100},
    )