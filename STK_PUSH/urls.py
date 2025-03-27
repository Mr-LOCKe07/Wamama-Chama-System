from . import views
from django.urls import path
from.views import initiate_payment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('pay', views.pay, name='pay'),
        path('stk', views.MPESA, name="MPESA"),
        path('method', views.method, name="method"),
        path('kcb',views.kcb, name="kcb"),
        path('equity',views.equity, name="equity"),
        path('pesapal',views.pesapal, name="pesapal"),
        path('paypal',views.paypal, name="paypal"),
        # path("create-order/", create_order, name="create_order"),
        # path("capture-order/", capture_order, name="capture_order"),
        path("initiate-payment/", views.initiate_payment, name="initiate_payment"),
        path('home',views.index, name="home"),
        path('events',views.events, name="events"),
        path('calendar',views.calendar, name="calendar"),
        path('admin_sign',views.admin_sign, name="admin_sign"),
        path('',views.sign_up, name="sign_up"),
        path('meetings',views.meetings, name="meetings"),
        # path('dashboard',views.dashboard,name="dashboard"),
        path('add_meeting/', views.add_meeting, name='add_meeting'),
        path('meeting/<int:meeting_id>/', views.meeting_detail, name='meeting_detail'),
        path('articles', views.articles, name='articles'),
        path('delete-meeting/<int:meeting_id>/', views.delete_meeting, name='delete-meeting'),
        path('register/', views.register, name="register"),
        path('login/', views.user_login, name="login"),
        path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
        path('admin_login/',views.admin_login, name="admin_login"),
        path('logout/',views.logout, name="logout"),
        path('user_logout/',views.user_logout, name="user_logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
