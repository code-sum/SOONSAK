from django.shortcuts import render, redirect
from .forms import ReviewForm, CommentForm
from .models import Review, Comment

# Create your views here.

# 글 목록
def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews' : reviews
    }
    return render(request, 'reviews/index.html', context)

# 글 작성
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews:index')
    else:
        form = ReviewForm()
    context = {
        'form' : form
    }
    return render(request, 'reviews/create.html', context)

# 글 조회
def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm()
    context = {
        'review' : review,
        'comment_form' : comment_form
    }
    return render(request, 'reviews/detail.html', context)

# 글 수정
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:detail', review_pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form' : form
    }
    return render(request, 'reviews/update.html', context)

# 글 삭제
def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    review.delete()
    return redirect('reviews:index')


# 댓글 작성
def add_comment(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
        return redirect('reviews:detail', review_pk)
    else:
        comment_form = CommentForm()
    context = {
        'comment_form' : comment_form
    }
    return render(request, 'reviews/add_comment.html', context)

# 댓글 삭제
def delete_comment(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('reviews:detail', review_pk)