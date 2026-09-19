"""
URL configuration for DIETPLANNER project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from rest_framework.authtoken import views as authview
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user',views.UserCreateView.as_view()),
    path('token',authview.obtain_auth_token),
    path('profile',views.ProfileCreateListView.as_view()),
    path('detail',views.ProfileDetailView.as_view()),
    path('foodlog',views.FoodLogCreateListView.as_view()),
    path('foodlog/detail/<int:id>',views.FoodLogDetailView.as_view()),
    path('access',TokenObtainPairView.as_view()),
    path('refresh',TokenRefreshView.as_view()),
    path('food/scan',views.FoodScanView.as_view()),
    path('diet/plan',views.DietPlanView.as_view()),
    path('summary',views.SummaryView.as_view()),
    path('payment/create',views.PaymentCreateView.as_view()),
    path('payment/verify',views.VerifyPayment.as_view()),
]
