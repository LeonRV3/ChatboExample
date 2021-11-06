from django.urls import re_path
from .views import trainModel,testModel,activateModel

urlpatterns = [
    re_path(r"^train/?$",trainModel.as_view()),
    re_path(r"^test/?$",testModel.as_view()),
    re_path(r"^activate/?$",activateModel.as_view())
]