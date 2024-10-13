from rest_framework import serializers
from posts.models import Post, Category, SearchWord
from rest_framework.exceptions import ValidationError


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


class PostValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=255)
    text = serializers.CharField(required=False)
    is_active = serializers.BooleanField()
    view_count = serializers.IntegerField(min_value=0, max_value=100)
    category_id = serializers.IntegerField(min_value=1)
    search_words = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category_id

    def validate_search_words(self, search_words):
        search_words_db = SearchWord.objects.filter(id__in=search_words)
        if len(search_words_db) != len(search_words):
            raise ValidationError('Search word does not exist')
        return search_words

    # def validate(self, attrs):
    #     category_id = attrs.get('category_id')
    #     try:
    #         Category.objects.get(id=category_id)
    #     except Category.DoesNotExist:
    #         raise ValidationError('Category does not exist!')
    #
    #     return attrs
