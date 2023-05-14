from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
      try:
        data = request.data
        serializer = BlogSerializer(data = data)
      except Exception as e:
        return Response({
                'data': {},
                'message': 'something went wrong',
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)