from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-request/', views.create_request, name='create_request'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('leave-review/<int:request_id>/', views.leave_review, name='leave_review'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]