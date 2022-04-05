from django.urls import path

from . import views

urlpatterns = [
    # User Account Functionalities
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('resetpassword_validate/<uidb64>/<token>/',
         views.resetpassword_validate, name='resetpassword_validate'),
    # ...

    # Dashboard and Profile
    path('', views.dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # ...

    # My Orders and Details
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<int:order_id>/',
         views.order_detail, name='order_detail'),
    # ...

    #     celery tests
    #     path('test/', views.test, name='test'),
    #     path('send-mail-to-all/', views.send_mail_to_all, name='send_mail_to_all'),
    # ...

]
