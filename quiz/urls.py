from django.urls import path
from .views import GenerateQuizView, xai_chat

urlpatterns = [
    path('quiz/generate/', GenerateQuizView.as_view(), name='generate-quiz'),
    path('xai/chat/', xai_chat, name='xai_chat'),
]