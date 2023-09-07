from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework_simplejwt.views import TokenVerifyView
from .views import userRegisterAPIViews, MyObtainTokenPairView

urlpatterns = [

    # registration using api call
    path('user-register-api/', userRegisterAPIViews.as_view(),
         name="user-register-api "),
    # creating token after userlogin

    path('create-token-api/', MyObtainTokenPairView.as_view(),
         name='create-token'),

    # getting access token using refresh-token after expired
    path('gettoken/refresh/', TokenRefreshView.as_view(),
         name='gettoken'),



]
