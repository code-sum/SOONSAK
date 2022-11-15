from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# 회원가입 폼
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 
            'username',
            'password1',
            'password2',
            'profile_image',
            'address',
            'phone_num',
        ]
        labels = {"username": "아이디", "profile_image":"프로필 이미지", "address": "주소", "phone_num": "연락처"}
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['password1']:
            self.fields[fieldname].help_text = None
print(CustomUserCreationForm())

# 회원 프로필수정 폼
class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=(""),
        help_text=''
        )
    class Meta:
        model = get_user_model()
        fields = [
            'profile_image',
            'address',
        ]
        labels = {"profile_image":"프로필 이미지 변경","address": "주소 변경", "phone_num":"연락처 변경"}

# 회원 비밀번호수정 폼
class CustomPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=("새 비밀번호"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=None
        )