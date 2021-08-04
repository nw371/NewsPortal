from django.contrib.auth.models import User
from django.db import models

class Authors(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    authors_rating = models.IntegerField(default=0)

    def update_rating(self):
        #отфильтровываем все посты авотра и тянем рейтинги постов и умножаем на 3
        #отфильтровываем все коменты авотра и тянем их рейтинги
        #отфильтровываем все коменты к статьям автора и тянем их рейтинги
        #всё это суммируем
        #сохраняем в рейтинг автора
        pass

class Category(models.Model):
    category_name = models.CharField(max_length=32, default='Категория без названия')

class Post(models.Model):
    #связь «один ко многим» с моделью Author;
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    #поле с выбором — «статья» или «новость»;
    type_of_post = models.TextChoices('type_of_post', 'Статья Новость')
    # автоматически добавляемая дата и время создания;
    time_of_pub = models.DateTimeField(auto_now_add=True)
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    products = models.ManyToManyField(Category, through='PostCategory')
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
    text_of_comment = models.TextField()
    # дата и время создания комментария;
    time_of_comment = models.DateTimeField(auto_now_add=True)
    # рейтинг комментария.
    rating_of_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_of_comment += 1
        self.save()
    def dislike(self):
        self.rating_of_comment -= 1
        self.save()

# SHELL COMMANDS
# >>> from django.contrib.auth.models import User
# >>> user1 = User.objects.create_user(username="User Name 1", password="UN1pass")
# >>> user2 = User.objects.create_user(username="User Name 2", password="UN2pass")
# >>> from news.models import Authors
# >>> author1 = Authors.objects.create(author=user1)
# >>> author2 = Authors.objects.create(author=user2)
# >>> from news.models import Category
# >>> cat1 = Category.objects.create(category_name='Микроэлектроника')
# >>> cat2 = Category.objects.create(category_name='Робототехника')
# >>> cat3 = Category.objects.create(category_name='Софт')
# >>> cat4 = Category.objects.create(category_name='Промышленность 4.0')
