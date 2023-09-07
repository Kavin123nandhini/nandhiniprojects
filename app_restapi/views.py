# from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import userSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserRegistration
from rest_framework.permissions import AllowAny
from rest_framework import generics


# Create your views here.
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class userRegisterAPIViews(generics.ListCreateAPIView):
    queryset = UserRegistration.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = userSerializer


