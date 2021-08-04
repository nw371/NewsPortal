from django.contrib.auth.models import User
from django.db import models

class Authors(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    authors_rating = models.IntegerField(default=0)

class Category(models.Model):
    microelectronics = 'ME'
    robotics = 'RO'
    industry4 = 'I4'
    software = 'Sw'
    other = 'GR'
    Category_CHOICES = [
        (microelectronics, 'Микроэлектроника'),
        (robotics, 'Робототехника'),
        (industry4, 'Индустрия 4.0'),
        (software, 'Программное обеспечение'),
        (other, 'Разное'),
    ]
    category_name = models.CharField(
        max_length=2,
        choices=Category_CHOICES,
        default=other,
        unique=True,
    )

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