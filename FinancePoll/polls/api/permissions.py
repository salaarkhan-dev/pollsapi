from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404
from polls.models import Question


class IsMultipleChoiceQuestion(BasePermission):
    message = "This isn't a multiple choice question."

    def has_permission(self, request, view):
        question_pk = view.kwargs.get('question_pk')
        question = get_object_or_404(Question, pk=question_pk)
        if question.question_type == 'multiple_choice':
            return True
        return False


class IsNumericQuestion(BasePermission):
    message = "This isn't a numeric question."

    def has_permission(self, request, view):
        question_pk = view.kwargs.get('question_pk')
        question = get_object_or_404(Question, pk=question_pk)
        if question.question_type == 'numeric_input':
            return True
        return False


class IsDateQuestion(BasePermission):
    message = "This isn't a date type question."

    def has_permission(self, request, view):
        question_pk = view.kwargs.get('question_pk')
        question = get_object_or_404(Question, pk=question_pk)
        if question.question_type == 'date_input':
            return True
        return False
