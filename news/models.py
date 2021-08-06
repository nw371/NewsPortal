from django.contrib.auth.models import User
from django.db import models

class Authors(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    authors_rating = models.IntegerField(default=0)

    def update_rating(self,authors_name):
        #отфильтровываем все посты автора и тянем рейтинги постов, суммируем их и умножаем на 3
        all_posts = Post.objects.filter(author = authors_name).values('post_rating')
        all_posts = sum(all_posts)*3
        #отфильтровываем все коменты автора и тянем их рейтинги
        all_authors_comments = Comment.objects.filter(user = authors_name).values('comment_rating')
        all_authors_comments = sum(all_authors_comments)
        #отфильтровываем все коменты к статьям автора и тянем их рейтинги
        all_posts_comments = Comment.objects.filter(post = authors_name).values('comment_rating')
        all_posts_comments = sum(all_posts_comments)

        #всё это суммируем
        authors_rating = all_posts + all_authors_comments + all_posts_comments
        #сохраняем в рейтинг автора
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=32, default='Категория без названия')

class Post(models.Model):
    #связь «один ко многим» с моделью Author;
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    #поле с выбором — «статья» или «новость»;
    post_type = models.TextChoices('post_type', 'СТАТЬЯ НОВОСТЬ')
    # автоматически добавляемая дата и время создания;
    post_time = models.DateTimeField(auto_now_add=True)
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    post_category = models.ManyToManyField(Category, through='PostCategory')
    # заголовок статьи/новости;
    post_name =  models.CharField(max_length=255, default='Пустой заголовок')
    # текст статьи/новости;
    post_body = models.TextField(default='Пустое сообщение')
    # рейтинг статьи/новости.
    post_rating = models.IntegerField(default=0)

    def preview(self):
        post_preview = self.post_body[:124]+"..."
        return post_preview

    def like(self):
        self.post_rating += 1
        self.save()
    def dislike(self):
        self.post_rating -= 1
        self.save()

class PostCategory(models.Model):
    # связь «один ко многим» с моделью Post;
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» с моделью Category.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    # связь «один ко многим» с моделью Post;
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» с встроенной моделью User (комментарии может оставить любой пользователь, не обязательно автор);
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # текст комментария;
    comment_text = models.TextField()
    # дата и время создания комментария;
    comment_time = models.DateTimeField(auto_now_add=True)
    # рейтинг комментария.
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()
    def dislike(self):
        self.comment_rating -= 1
        self.save()

# SHELL COMMANDS
# from django.contrib.auth.models import User
# from news.models import Authors
# from news.models import Category
# from news.models import Post
# from news.models import PostCategory
# from news.models import Comment

# user1 = User.objects.create_user(username="UserName1", password="UN1pass", first_name = "User1", last_name = "Name1")
# user2 = User.objects.create_user(username="UserName2", password="UN2pass", first_name = "User2", last_name = "Name2")
# user3 = User.objects.create_user(username="UserName3", password="UN3pass", first_name = "User3", last_name = "Name3")
#
# author1 = Authors.objects.create(author=user1)
# author2 = Authors.objects.create(author=user2)
# author3 = Authors.objects.create(author=user3)

# cat1 = Category.objects.create(category_name='Микроэлектроника')
# cat2 = Category.objects.create(category_name='Робототехника')
# cat3 = Category.objects.create(category_name='Софт')
# cat4 = Category.objects.create(category_name='Промышленность 4.0')

# post1 = Post.objects.create(author = author1, post_type.choices['СТАТЬЯ'], post_category = cat1, post_name = 'Новые процессоры "Эльбрус"', post_body = 'Длинный текст с описанием последнего поколения процессоров')
# post1 = Post.objects.create(author = author1, post_category = cat1, post_name = 'Новые процессоры "Эльбрус"', post_body = 'Длинный текст с описанием последнего поколения процессоров', post_type.choices['СТАТЬЯ'], )
# post1 = Post.objects.create(post_type.choices['СТАТЬЯ'], author = author1, post_category = cat1, post_name = 'Новые процессоры "Эльбрус"', post_body = 'Длинный текст с описанием последнего поколения процессоров')