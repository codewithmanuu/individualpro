from django.urls import path
from .views import *
urlpatterns=[
    path('regis/',regis),
    path('verify/<auth_token>',verify),
    path('login/',login),
    path('off/',off),
    path('dreg/',dregister),
    path('dlog/',dlog),
    path('ortho/',orthofileup),
    path('oview/',ofupd),
    path('chome/',home,name="home"),
    path('<str:room>/',room,name="room"),
    path('checkview',checkview,name="checkview"),
    path('send',send,name="send"),
    path('get', getmsg, name="get"),
    path('uroom/<int:id>',uroom),
    # path('main',main, name="main"),


]