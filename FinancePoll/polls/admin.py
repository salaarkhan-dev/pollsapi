from django.contrib import admin
from .models import (
    Poll,
    Question,
    Choice,
    Answer,
    Bit,
    Product,
    SessionProfile
)
# Register your models here.


class ChoicesInline(admin.TabularInline):
    model = Choice


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = [
        'poll_name',
        'published',
    ]
    list_filter = ('poll_name', 'published')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'question_text',
        'poll',
        'published',
        'pub_date'
    ]
    inlines = [
        ChoicesInline,
    ]
    list_filter = ('question_text', 'poll', 'published', 'pub_date')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'session_id',
        'poll',
        'question',
        'choice',
        'numeric_answer',
    ]

    list_filter = ('session_id', 'poll', 'question')


@admin.register(Bit)
class BitAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'risk_value',
        'published',
    ]

    list_filter = ('name', 'risk_value', 'published')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'bit'
    ]
    list_filter = ('name', 'bit')


@admin.register(SessionProfile)
class SessionProfileAdmin(admin.ModelAdmin):
    list_display = [
        'session_id',
        'poll',
        'bit',
        'creation_date',
    ]

    list_filter = ('session_id', 'poll', 'bit', 'creation_date')
