from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from .models import Blog
from django.db.models import Q
# Create your views here.

class PublicBlog(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')
            
            # Filtering blogs based on search query
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))
                
            page_number = request.GET.get('page', 1)
            # sending 3 blog posts from the database
            paginator = Paginator(blogs, 3)
            serializer = BlogSerializer(paginator.page(page_number), many=True)
            
            return Response({
                'data': serializer.data,
                'message': 'Blogs fetched successfully✅'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong or invalid page.',
            }, status=status.HTTP_400_BAD_REQUEST)

    
  

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # * Get all the blog posts that a user has created.
    def get(self, request):
      try:
        blogs = Blog.objects.filter(user = request.user)
        # * http://127.0.0.1:8000/api/home/blog/?search=name
        if request.GET.get('search'):
          search = request.GET.get('search')
          blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))
        serializer = BlogSerializer(blogs, many  = True)
        return Response({
                    'data': serializer.data,
                    'message': 'Blogs fetched successfully✅'
                }, status=status.HTTP_400_BAD_REQUEST)
      except Exception as e:
        print(e)
        return Response({
                'data': {},    
                'message': 'something went wrong❌',
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
      try:
        data = request.data
        data['user'] = request.user.id
        serializer = BlogSerializer(data = data)

        if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong❌'
                }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
        'data': serializer.data,
          'message': 'Blog created successfully➕'
      }, status = status.HTTP_201_CREATED)
      except Exception as e:
        return Response({
                'data': {},    
                'message': 'something went wrong❌',
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)
      
    def patch(self, request):
      try:
          data = request.data
          blog = Blog.objects.filter(uid=data.get('uid'))
          if not blog.exists():
              return Response({
                  'data': {},    
                  'message': 'Invalid blog uid❌',
              }, status=status.HTTP_400_BAD_REQUEST)

          for blog_item in blog:
              if request.user != blog_item.user:
                  return Response({
                      'data': {},    
                      'message': 'You are not authorized to do this.❌',
                  }, status=status.HTTP_400_BAD_REQUEST)
            
              serializer = BlogSerializer(blog_item, data=data, partial=True)
              if not serializer.is_valid():
                  return Response({
                      'data': serializer.errors,
                      'message': 'Something went wrong❌'
                  }, status=status.HTTP_400_BAD_REQUEST)
              serializer.save()
              return Response({
                  'data': serializer.data,
                  'message': 'Blog updated successfully⛓'
              }, status=status.HTTP_201_CREATED)
          
      except ValueError as e:
          print(e)  # Consider using a logging library instead of print
          return Response({
              'data': {},    
              'message': 'Invalid data format❌',
          }, status=status.HTTP_400_BAD_REQUEST)
      
      except Exception as e:
          print(e)  # Consider using a logging library instead of print
          return Response({
              'data': {},    
              'message': 'Something went wrong❌',
          }, status=status.HTTP_400_BAD_REQUEST)
          
    def delete(self, request):
      try:
          data = request.data
          blog = Blog.objects.filter(uid=data.get('uid'))
          if not blog.exists():
              return Response({
                  'data': {},    
                  'message': 'Invalid blog uid❌',
              }, status=status.HTTP_400_BAD_REQUEST)

          if request.user != blog[0].user:
              return Response({
                  'data': {},    
                  'message': 'You are not authorized to do this.❌',
              }, status=status.HTTP_400_BAD_REQUEST)
                
          blog[0].delete()
          return Response({
              'data': {},    
              'message': 'Blog deleted successfully⛓'
          }, status=status.HTTP_200_OK)
      except Exception as e:
          print(e)  # Consider using a logging library instead of print
          return Response({
              'data': {},    
              'message': 'Something went wrong❌',
          }, status=status.HTTP_400_BAD_REQUEST)
