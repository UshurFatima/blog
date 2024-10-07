from rest_framework import serializers
from posts.models import Post, Category, SearchWord


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SearchWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchWord
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    search_words = SearchWordSerializer(many=True)
    category_name = serializers.SerializerMethodField()

    # данные которые не будут меняться
    class Meta:
        model = Post
        # поля, которые мы хотим видеть
        fields = 'id comments category category_name search_words search_word_list title view_count created'.split()  # ['id', 'title', ...]
        # fields = '__all__'
        # exclude = 'created text'. split()

        # depth = 1

    def get_category_name(self, post):
        return post.category.name if post.category else None
