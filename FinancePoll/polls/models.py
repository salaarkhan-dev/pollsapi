from django.utils.translation import gettext_lazy as _
from django.db import models


class Poll(models.Model):
    poll_name = models.CharField(max_length=50)
    poll_description = models.CharField(max_length=1000, blank=True)
    published = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.poll_name


class Question(models.Model):
    TYPE = (
        ("multiple_choice", _('Multiple Choice')),
        ("numeric_input", _('Numeric Input')),
        ("date_input", _('Date Input')),
    )

    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=1000, blank=False, null=False)
    question_type = models.CharField(max_length=50, choices=TYPE,
                                     verbose_name=_("Type of Question"))
    pub_date = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=1)
    published = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['order', 'id']

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200, null=True)
    value = models.IntegerField()

    def __str__(self):
        return self.choice_text.upper()


class NumericChoice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='numeric_input')
    choice_text = models.FloatField(blank=True)

    def __str__(self):
        return self.choice_text.upper()


class DateChoice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='date_input')
    date = models.DateField(blank=True)

    def __str__(self):
        return self.date


class Answer(models.Model):

    session_id = models.CharField(max_length=500)
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name='answers_poll')
    question = models.ForeignKey(
        Question, related_name='answers', on_delete=models.CASCADE)
    choice = models.ForeignKey(
        Choice, related_name='answer', on_delete=models.CASCADE, blank=True, null=True)
    numeric_answer = models.IntegerField(blank=True, null=True)
    date_answer = models.DateField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ['id']
        unique_together = ["session_id", "question", "poll"]

    def __str__(self):
        return self.session_id

    @property
    def score(self):
        if self.choice:
            return self.choice.value


class Bit(models.Model):
    name = models.CharField(max_length=100)
    poll = models.ManyToManyField(
        Poll, related_name="bits")
    short_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    how_invest = models.TextField(blank=True)
    motto = models.CharField(max_length=500, blank=True)
    behavioral_biases = models.CharField(max_length=200, blank=True)
    cognitive_biases = models.CharField(max_length=200, blank=True)
    risk_value = models.IntegerField(default=0)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    aktien = models.FloatField(blank=True, default=0)
    anleihen = models.FloatField(blank=True, default=0)
    investment_horizon = models.FloatField(blank=True, default=0)
    experience = models.FloatField(blank=True, default=0)
    liquidity_needs = models.FloatField(blank=True, default=0)
    bit = models.ForeignKey(
        Bit, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.short_name


class SessionProfile(models.Model):
    '''Calculated profile for user'''
    session_id = models.CharField(max_length=200)
    poll = models.ForeignKey(
        Poll, on_delete=models.PROTECT, related_name='profiles')
    bit = models.ForeignKey(
        Bit, on_delete=models.PROTECT, related_name='bit')
    products = models.ManyToManyField(Product, related_name="products")
    user_rating = models.IntegerField(blank=True, default=0)
    profile_calc = models.FloatField(blank=True, default=0)
    potential_investment = models.FloatField(blank=True, default=0)
    horizon = models.FloatField(blank=True, default=0)
    liquidity_needs = models.FloatField(blank=True, default=0)
    investment_experience_years = models.FloatField(blank=True, default=0)
    investment_previous = models.FloatField(blank=True, default=0)
    accepts_profile = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.poll.poll_name

    class Meta:
        unique_together = ["session_id", "poll"]
