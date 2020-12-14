from django.urls import path
from .views import (
    PollListAPIView,
    PollDetailAPIView,
    QuestionListAPIView,
    QuestionDetailAPIView,
    AnswerMultipleCreateAPIView,
    AnswerNumericCreateAPIView,
    AnswerDateCreateAPIView,
    AnswerListAPIView,
    SessionProfileListAPIView
)

urlpatterns = [

    path('',
         PollListAPIView.as_view(),
         name='poll-list'),

    path('<int:poll_pk>/',
         PollDetailAPIView.as_view(),
         name='poll-detail'),

    path('<int:poll_pk>/questions/',
         QuestionListAPIView.as_view(),
         name='question-list'),

    path('<int:poll_pk>/answers/',
         AnswerListAPIView.as_view(),
         name='answer-list'),

    path('<int:poll_pk>/result/',
         SessionProfileListAPIView.as_view(),
         name='sessionprofile-list'),

    path('<int:poll_pk>/questions/<int:question_pk>/',
         QuestionDetailAPIView.as_view(),
         name='question-detail'),

    path('<int:poll_pk>/questions/<int:question_pk>/<int:choice_pk>/answer/',
         AnswerMultipleCreateAPIView.as_view(),
         name='question-choices-answer'),

    path('<int:poll_pk>/questions/<int:question_pk>/numericanswer/',
         AnswerNumericCreateAPIView.as_view(),
         name='question-numeric-answer'),

    path('<int:poll_pk>/questions/<int:question_pk>/dateanswer/',
         AnswerDateCreateAPIView.as_view(),
         name='question-date-answer'),
]
