from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    # данные которые не будут меняться
    class Meta:
        model = Post
        # поля, которые мы хотим видеть
        fields = 'id title view_count created'.split()  # ['id', 'title', ...]
        # fields = '__all__'
        # exclude = 'created text'. split()

