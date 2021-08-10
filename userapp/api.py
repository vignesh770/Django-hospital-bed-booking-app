from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import UserSerializer


class UserDetailsAPIView(GenericAPIView):

    def get(self, request):
        user = request.user

        if user:
            serialized_data = UserSerializer(user)
            return Response(serialized_data.data)




