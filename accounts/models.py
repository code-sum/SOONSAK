from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import RegexValidator

class User(AbstractUser):

    pass
    # 소셜 로그인
    kakao_id = models.BigIntegerField(null=True, unique=True)
    naver_id = models.CharField(null=True, unique=True, max_length=100)
    # googld_id = models.CharField(null=True, unique=True, max_length=50)
    # 회원가입 주소
    address = models.CharField(max_length=250)
    # 회원가입 연락처
    phone_numRegex = RegexValidator(regex= r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone_num = models.CharField(validators= [phone_numRegex], max_length=11, blank=True, null=True, default="")
    # 팔로윙
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    # 프로필_이미지
    profile_image = ProcessedImageField(
        upload_to="images/accounts/",
        blank=True,
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 100},
    )