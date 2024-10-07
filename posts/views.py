from rest_framework.decorators import api_view
# проверяет http_methods и какие может принимать функция
# если подходят, то функция работает
# api - Application Programming Interface (доступ)
from rest_framework.response import Response
# ответ на запрос: данные (список/JSON) статус запроса (100, 200, 300, 400, 500)
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import status


# доступ к получению данных
@api_view(http_method_names=['GET'])
def post_list_api_view(request):
    # step 1: Collect data(posts) -> Queryset
    #                    один объект                несколько объектов
    posts = Post.objects.select_related('category').prefetch_related('search_words', 'comments').all()

    # step 2: Reformat posts to list of Dictionaries (JSON)
    data = PostSerializer(instance=posts, many=True).data

    # list_ = []
    # for post in posts:
    #     list_.append({
    #         'id': post.id,
    #         'title': post.title,
    #         'text': post.text,
    #         'is_active': post.is_active
    #     })

    # step 3: Return response as JSON
    return Response(data=data)


# информация только об одном объекте
@api_view(http_method_names=['GET'])
def post_detail_api_view(request, id):
    # step 1: Collect data(posts) -> Queryset
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)

    # step 2: Reformat posts to list of Dictionaries (JSON)
    data = PostSerializer(instance=post, many=False).data

    # step 3: Return response as JSON
    return Response(data=data)
