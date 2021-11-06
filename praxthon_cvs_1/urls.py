"""praxthon_cvs_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,re_path
from django.urls.conf import include
from rest_framework import routers
from webapp import views as wviews
from chatbot import views as cviews

router = routers.DefaultRouter()
router.register(r'productos',wviews.ProductoViewSet)
router.register(r'conversation',cviews.conversationViewSet)
router.register(r'conversation_samples',cviews.conversationSamplesViewSet)
router.register(r'response',cviews.responseViewSet)
router.register(r'response_samples',cviews.responseSamplesViewSet)
router.register(r'intent',cviews.intentViewSet)
router.register(r'intent_samples',cviews.intentSamplesViewSet)

urlpatterns = [
    re_path('^REST/', include(router.urls)),
    re_path('^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    re_path('^$',include('frontend.urls')),
    re_path('^search/',include('webapp.urls')),
    re_path('^chatbot/',include('chatbot.urls'))
]
