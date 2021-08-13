from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_sum_rating = Post.objects.filter(post_author = self.author_user).values("post_rating")
        comments_sum_rating = Comment.obejects.filter(user = self.author_user).values("comment_rating")
        post_comments_sum_rating = Comment.obejects.filter(Post, user = self.author_user).values("comment_rating")
        self.author_rating = posts_sum_rating*3 + comments_sum_rating + post_comments_sum_rating
        self.save()

class Category(models.Model):
    Industry4 = "I4"
    Robotics = "RO"
    IoT = "IO"
    Automation = "AU"
    Non = "NO"

    CATEGORIES =[
        (Industry4, "Промышленность 4.0"),
        (Robotics, "Роботы"),
        (IoT, "Интернет вещей"),
        (Automation, "Автоматизация"),
        (Non, "Без категории"),
    ]

    category = models.CharField(max_length=2, choices=CATEGORIES, unique=True, default=Non)


class Post(models.Model):
    post_header = models.CharField(max_length=255, default="Без названия")
    post_body = models.TextField(default="Ожидает публикации")
    post_rating = models.IntegerField(default=0)
    post_date = models.DateField(auto_now_add=True)
    post_type = models.TextChoices('post_type', 'СТАТЬЯ НОВОСТЬ')

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        post_preview = self.post_body[:124]
        return f"{post_preview}..."

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_body = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
