from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from orders.models import Order
from snacks.models import Snack
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count

# 리뷰 목록
def index(request):
    reviews = Review.objects.order_by("-created_at")
    context = {"reviews": reviews}
    return render(request, "reviews/index.html", context)


@login_required(login_url="accounts:login")
def create(request, snack_pk):
    snack = get_object_or_404(Snack, pk=snack_pk)
    # 구매자만 리뷰 작성 가능
    orders = Order.objects.filter(
        user__id=request.user.pk,
        snack__id=snack_pk,
        order_status="결제완료",
    ).exists()
    if orders:
        if request.method == "POST":
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.snack = snack
                review.save()
                return redirect("snacks:detail", snack_pk)
        else:
            form = ReviewForm()
        context = {"form": form}
        return render(request, "reviews/create.html", context)
    else:
        messages.error(request, "제품을 구매한 사용자만 리뷰를 작성할 수 있습니다.")
        return redirect("snacks:detail", snack_pk)


# 리뷰 조회
@login_required(login_url="accounts:login")
def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    # 별점 가져오기
    grade = review.grade
    if grade == 5:
        star = "⭐⭐⭐⭐⭐"
    elif grade == 4:
        star = "⭐⭐⭐⭐"
    elif grade == 3:
        star = "⭐⭐⭐"
    elif grade == 2:
        star = "⭐⭐"
    elif grade == 1:
        star = "⭐"

    comment_form = CommentForm()
    context = {
        "review": review,
        "comment_form": comment_form,
        "star": star,
    }
    return render(request, "reviews/detail.html", context)


# 리뷰 수정
@login_required(login_url="accounts:login")
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    snack = Snack.objects.get(pk=review.snack.pk)

    if review.user != request.user:
        messages.error(request, "작성자만 수정할 수 있습니다.")
        return redirect("snacks:detail", snack.pk)

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect("reviews:detail", review_pk)
    else:
        form = ReviewForm(instance=review)
    context = {"form": form}
    return render(request, "reviews/update.html", context)


# 리뷰 삭제
@login_required(login_url="accounts:login")
def delete(request, review_pk):

    review = Review.objects.get(pk=review_pk)
    snack = Snack.objects.get(pk=review.snack.pk)
    if review.user != request.user:
        messages.error(request, "작성자만 삭제할 수 있습니다.")
        return redirect("snacks:detail", snack.pk)

    review.delete()
    return redirect("snacks:detail", snack.pk)


# 댓글 작성
@login_required(login_url="accounts:login")
def add_comment(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
        return redirect("reviews:detail", review_pk)
    else:
        comment_form = CommentForm()
    context = {"comment_form": comment_form}
    return render(request, "reviews/add_comment.html", context)


# 댓글 삭제
@login_required(login_url="accounts:login")
def delete_comment(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect("reviews:detail", review_pk)
