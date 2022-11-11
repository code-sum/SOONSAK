from django.urls import path
from . import views

app_name = 'snacks'

urlpatterns = [
  path("detail/<int:snack_pk>", views.detail, name="detail"),
  path("delete/<int:snack_pk>", views.delete, name="delete"),

]