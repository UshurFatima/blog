from django.db import models


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(AbstractModel):
    pass


class SearchWord(AbstractModel):
    pass


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)  # category_id
    # для ManyToManyField - отдельная таблица
    search_words = models.ManyToManyField(SearchWord, blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def search_word_list(self):
        return [i.name for i in self.search_words.all()]


STARS = (
    (1, '*'),
    (2, '* *'),
    (3, '* * *'),
    (4, '* * * *'),
    (5, '* * * * *'),
)


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    stars = models.IntegerField(choices=STARS, default=5)

    def __str__(self):
        return self.text
