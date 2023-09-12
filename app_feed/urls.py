from django.urls import path

from . import views

urlpatterns = [

    path('search-friends/', views.search_friends, name="search-friends"),
    path('add-friend/', views.add_friend, name="add-friend"),
    path('send-message/', views.send_message, name='send-message'),
    path('accept-friend-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-friend-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('post-job/', views.post_job, name='post-job'),
    path('jobs-page/', views.jobs_page, name='jobs-page'),
    path('view-job/<int:id>/', views.view_job, name='view-job'),
    path('apply-job/<int:id>/', views.apply_job, name='apply-job'),
    path('view-applied-list/', views.view_applied_list, name='view-applied-list'),
    path('cancel-applied/<int:id>/',views.cancel_applied,name='cancel-applied'),

    path('accept-result/<int:id>',views.accept_result,name='accept-result'),
    path('ignore-result/<int:id>',views.ignore_result,name='ignore-result'),
    path('hold-result/<int:id>',views.hold_result,name='hold-result'),

]
