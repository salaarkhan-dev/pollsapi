from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (AllowAny,)

from rest_framework.generics import get_object_or_404
from .paginations import SmallSetPagination

from polls.models import (
    Poll,
    Question,
    Answer,
    SessionProfile
)

from .serializers import (
    PollListSerializer,
    PollDetailSerializer,
    QuestionListSerializer,
    QuestionDetailSerializer,
    AnswerMultipleCreateSerializer,
    AnswerNumericCreateSerializer,
    AnswerDateCreateSerializer,
    AnswerListSerializer,
    SessionProfileListSerializer
)

from .permissions import (
    IsMultipleChoiceQuestion,
    IsNumericQuestion,
    IsDateQuestion
)


class PollListAPIView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollListSerializer
    permission_classes = [AllowAny]
    pagination_class = SmallSetPagination
    filter_backends = [SearchFilter]
    search_fields = ["poll_name", "poll_description"]

    def get_queryset(self):
        queryset = Poll.objects.all()
        queryset = queryset.filter(published=True)
        return queryset


class PollDetailAPIView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'poll_pk'


class QuestionListAPIView(generics.ListAPIView):
    serializer_class = QuestionListSerializer
    permission_classes = [AllowAny]
    pagination_class = SmallSetPagination

    def get_queryset(self):
        poll_pk = self.kwargs.get('poll_pk')
        poll = get_object_or_404(Poll, pk=poll_pk)
        queryset = Question.objects.all()
        queryset = queryset.filter(published=True, poll=poll)
        return queryset


class QuestionDetailAPIView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'question_pk'


class AnswerMultipleCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerMultipleCreateSerializer
    permission_classes = [IsMultipleChoiceQuestion, ]


class AnswerNumericCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerNumericCreateSerializer
    permission_classes = [IsNumericQuestion]


class AnswerDateCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerDateCreateSerializer
    permission_classes = [IsDateQuestion]


class AnswerListAPIView(generics.ListAPIView):
    serializer_class = AnswerListSerializer
    permission_classes = [AllowAny]  # NotNecessory
    pagination_class = SmallSetPagination

    def get_queryset(self):
        poll_pk = self.kwargs.get('poll_pk')
        poll = get_object_or_404(Poll, pk=poll_pk)
        request = self.request
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        queryset = Answer.objects.all()
        queryset = queryset.filter(session_id=session_id, poll=poll)
        return queryset


class SessionProfileListAPIView(generics.ListCreateAPIView):
    serializer_class = SessionProfileListSerializer
    permission_classes = [AllowAny]  # NotNecessory

    def get_queryset(self):
        poll_pk = self.kwargs.get('poll_pk')
        poll = get_object_or_404(Poll, pk=poll_pk)
        request = self.request
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        queryset = SessionProfile.objects.all()
        queryset = queryset.filter(session_id=session_id, poll=poll)
        return queryset
