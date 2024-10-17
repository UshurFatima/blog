from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserCreateSerializer, UserAuthSerializer


class AuthAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'error': 'User credentials are wrong!'})


# @api_view(['POST'])
# def authorization_api_view(request):
    # serializer = UserAuthSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    #
    # user = authenticate(**serializer.validated_data)
    # if user:
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response(data={'key': token.key})
    # return Response(status=status.HTTP_401_UNAUTHORIZED,
    #                 data={'error': 'User credentials are wrong!'})


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(username=username, password=password)
    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})
