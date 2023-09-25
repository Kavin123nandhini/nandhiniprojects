from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import jwt
from PostMan.settings import SIMPLE_JWT
import requests as req2
import json

register_api_url = "http://127.0.0.1:8000/app-restapi/user-register-api/"
user_create_api= "http://127.0.0.1:8000/app-restapi/user-create-api/"
login_api_url = "http://127.0.0.1:8000/app-restapi/create-token-api/"
get_access_token_url = "http://127.0.0.1:8000/app-restapi/gettoken/refresh/"



def get_user(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None


def get_datetime():
    # time = datetime.datetime.utcnow().strftime('%H:%M:%S')
    return datetime.datetime.utcnow()


"""
Expiration time will be compared to the current UTC time 
(as given by timegm(datetime.now(tz=timezone.utc).utctimetuple())), 
so be sure to use a UTC timestamp or datetime in encoding.
"""


def decode_payload(token: str):
    payload = None
    try:
        payload = jwt.decode(
            token,
            SIMPLE_JWT['SIGNING_KEY'],
            algorithms=[SIMPLE_JWT['ALGORITHM']], )
    except jwt.ExpiredSignatureError:
        print("token expired")
        # Raised when a token’s exp claim indicates that it has expired
        payload = "Expired"
    except jwt.InvalidTokenError:
        raise "No key found for this token"
    return payload


def check_access_token(access_token: str):
    payload = decode_payload(access_token)
    print("payload:", payload)
    if payload == "Expired":
        print("access token Expired")
        return True
    return False


def check_refresh_token(refresh_token: str):
    payload = decode_payload(refresh_token)
    print("payload:", payload)
    if payload == "Expired":
        return True
    return False


def get_access_token(refresh_token: str):
    try:
        params = json.dumps({'refresh': refresh_token})
        res2 = req2.post(get_access_token_url, params,
                         headers={'Content-Type': 'application/json'})
        print("res2", res2)
        if res2.json().get("access", ""):
            access_token = res2.json()["access"]
            # print("new access token:", access_token)
            return access_token
        else:
            print("Access Token Not Created")
    except req2.exceptions.RequestException as e:
        raise SystemExit(e)
    return None


def is_authendicated(request):
    if not request.session.get('logged_in'):
        return False
    access = request.session['access_token']
    print("Access_token:", access)
    refresh = request.session['refresh_token']
    print(access)
    if check_refresh_token(refresh):
        print("refresh token expired")
        messages.info(request, 'Session Expired ,Please Login Again!')
        try:
            print("logging out")
            request.session.flush()
        except KeyError:
            pass
        return False
        # check whether token expired
    if check_access_token(access):
        access = get_access_token(refresh)
        request.session['access_token'] = access
        request.session.modified = True
    print("session:", access)
    return True

