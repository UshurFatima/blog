from rest_framework.decorators import api_view, permission_classes
# проверяет http_methods и какие может принимать функция
# если подходят, то функция работает
# api - Application Programming Interface (доступ)
from rest_framework.response import Response
# ответ на запрос: данные (список/JSON) статус запроса (100, 200, 300, 400, 500)
from posts.models import Post, Category, SearchWord
from posts.serializers import (PostSerializer, PostValidateSerializer,
                               CategorySerializer, SearchWordSerializer)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.viewsets import ModelViewSet


class SearchWordViewSet(ModelViewSet):
    queryset = SearchWord.objects.all()
    serializer_class = SearchWordSerializer
    lookup_field = 'id'
    pagination_class = PageNumberPagination


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()  # List of objects from db
    serializer_class = CategorySerializer  # Serializer inherited by ModelSerializer
    pagination_class = CustomPagination


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class PostListCreateAPIView(ListCreateAPIView):
    queryset = (Post.objects.select_related('category').
                prefetch_related('search_words', 'comments').all())
    serializer_class = PostSerializer

    def post(self, request):
        serializer = PostValidateSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data=serializer.errors)

        # step 1: Receive data from request body
        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        is_active = serializer.validated_data.get('is_active')
        view_count = serializer.validated_data.get('view_count')
        category_id = serializer.validated_data.get('category_id')
        search_words = serializer.validated_data.get('search_words')

        # step 2: Create post by received data
        post = Post.objects.create(
            title=title,
            text=text,
            is_active=is_active,
            view_count=view_count,
            category_id=category_id
        )
        post.search_words.set(search_words)
        post.save()

        # step 3: Return response with data and status
        return Response(status=status.HTTP_201_CREATED,
                        data={'post_id': post.id})


# доступ к получению данных
# @api_view(http_method_names=['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def post_list_create_api_view(request):
#     print(request.user)
#     if request.method == 'GET':
#         # print(request.query_params)
#         search = request.query_params.get('search', '')
#
#         # step 1: Collect data(posts) -> Queryset
#         #                    один объект                несколько объектов
#         posts = (Post.objects.select_related('category')
#                  .prefetch_related('search_words', 'comments').filter(title__icontains=search))
#
#         # step 2: Reformat posts to list of Dictionaries (JSON)
#         data = PostSerializer(instance=posts, many=True).data
#
#         # list_ = []
#         # for post in posts:
#         #     list_.append({
#         #         'id': post.id,
#         #         'title': post.title,
#         #         'text': post.text,
#         #         'is_active': post.is_active
#         #     })
#
#         # step 3: Return response as JSON
#         return Response(data=data)
#
#     elif request.method == 'POST':
#         # step 0: Validation of data (existing, data type, extra)
#         serializer = PostValidateSerializer(data=request.data)
#         # serializer.is_valid(raise_exception=True)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                             data=serializer.errors)
#
#         # step 1: Receive data from request body
#         title = serializer.validated_data.get('title')
#         text = serializer.validated_data.get('text')
#         is_active = serializer.validated_data.get('is_active')
#         view_count = serializer.validated_data.get('view_count')
#         category_id = serializer.validated_data.get('category_id')
#         search_words = serializer.validated_data.get('search_words')
#
#         # step 2: Create post by received data
#         post = Post.objects.create(
#             title=title,
#             text=text,
#             is_active=is_active,
#             view_count=view_count,
#             category_id=category_id
#         )
#         post.search_words.set(search_words)
#         post.save()
#
#         # step 3: Return response with data and status
#         return Response(status=status.HTTP_201_CREATED,
#                         data={'post_id': post.id})


# информация только об одном объекте
@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def post_detail_api_view(request, id):
    # step 0: Validation of data (existing, data type, extra)
    serializer = PostValidateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                        data=serializer.errors)

    # step 1: Collect data(posts) -> Queryset
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(data={'error': 'Post not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # step 2: Reformat posts to list of Dictionaries (JSON)
        data = PostSerializer(instance=post, many=False).data

        # step 3: Return response as JSON
        return Response(data=data)

    elif request.method == 'PUT':
        post.title = serializer.validated_data.get('title')
        post.text = serializer.validated_data.get('text')
        post.is_active = serializer.validated_data.get('is_active')
        post.view_count = serializer.validated_data.get('view_count')
        post.category_id = serializer.validated_data.get('category_id')
        post.search_words.set(serializer.validated_data.get('search_words'))
        post.save()
        return Response(data=PostSerializer(post).data,
                        status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
