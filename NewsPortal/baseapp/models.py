from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_post = Post.objects.filter(author__pk=self.pk).aggregate(res_1=Sum('rating'))['res_1']
        rating_comments = Comment.objects.filter(user__pk=self.pk).aggregate(res_2=Sum('rating'))['res_2']
        rating_comm_post = 0
        for i in Post.objects.filter(author__pk=self.pk).values('pk'):
            k = Comment.objects.filter(post__pk=i['pk']).aggregate(res_3=Sum('rating'))['res_3']
            rating_comm_post += k
        self.rating = rating_post * 3 + rating_comments + rating_comm_post
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=75, unique=True)


class Post(models.Model):
    POSITIONS = [
        ('article', 'статья'),
        ('news', 'новость')
    ]

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    articles_news = models.CharField(max_length=8, choices=POSITIONS, default='news')
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    header = models.CharField(max_length=75, default='New post')
    text_news = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.header.title()}'
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text_news[:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.CharField(max_length=350)
    created_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
