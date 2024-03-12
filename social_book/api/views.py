
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, BookSerializer
from rest_framework.exceptions import AuthenticationFailed
from mainapp.models import CustomUser, Book
import jwt, datetime
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self,request):
        Serializer=UserSerializer(data=request.data)
        Serializer.is_valid(raise_exception=True)
        Serializer.save()
        return Response(Serializer.data)  #return is for responce
class LoginView(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']
        user=CustomUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationField("User Not Found")
        if not  user.check_password(password):
             raise AuthenticationField("Wrong Password")
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        response = Response()
        token=jwt.encode(payload,'secret',algorithm='HS256')
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data=({
            'jwt':token
        })
        return response
    
class UserView(APIView):
    # @login_required
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid token!')

        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class BookView(APIView):
    # @login_required
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid token!')
        book_obj = Book.objects.all()
        Serializer = BookSerializer(book_obj, many=True)
        return Response(Serializer.data)
    
class BookUploadAPIView(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid token!')
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class BookListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        book_obj = Book.objects.all()
        Serializer = BookSerializer(book_obj, many=True)
        return(Response({'status':200 ,'payload':Serializer.data}))
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response