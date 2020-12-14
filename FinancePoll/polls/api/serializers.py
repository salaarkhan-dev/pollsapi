from rest_framework import serializers
from polls.models import (
    Poll,
    Question,
    Choice,
    Answer,
    Bit,
    Product,
    SessionProfile
)
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime


class PollListSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()
    ago = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = (
            'id',
            'url',
            'poll_name',
            'poll_description',
            'published',
            'ago',
            'pub_date',
        )
        read_only_fields = ('pub_date',)

    def get_url(self, obj):
        return str(self.context['request'].build_absolute_uri(obj.id))

    def get_ago(self, obj):
        return naturaltime(obj.pub_date)


class QuestionHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'question-detail'
    queryset = Question.objects.all()

    def get_url(self, obj, view_name, request, format):

        url_kwargs = {
            'poll_pk': obj.poll.id,
            'question_pk': obj.id,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'poll__pk': view_kwargs['poll_pk'],
            'pk': view_kwargs['question_pk'],
        }
        return self.get_queryset().get(**lookup_kwargs)


class PollDetailSerializer(serializers.ModelSerializer):

    ago = serializers.SerializerMethodField()
    questions_url = serializers.SerializerMethodField()
    answers_url = serializers.SerializerMethodField()
    result_url = serializers.SerializerMethodField()
    questions = QuestionHyperlink(many=True)

    class Meta:
        model = Poll
        fields = (
            'id',
            'poll_name',
            'poll_description',
            'published',
            'questions_url',
            'answers_url',
            'result_url',
            'questions',
            'ago',
            'pub_date',
        )
        read_only_fields = ('pub_date',)

    def get_ago(self, obj):
        return naturaltime(obj.pub_date)

    def get_questions_url(self, obj):
        return str(self.context['request'].build_absolute_uri() + "questions")

    def get_answers_url(self, obj):
        return str(self.context['request'].build_absolute_uri() + "answers")

    def get_result_url(self, obj):
        return str(self.context['request'].build_absolute_uri() + "result")


class QuestionListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    ago = serializers.SerializerMethodField()
    poll = serializers.HyperlinkedRelatedField(view_name='poll-detail',
                                               read_only=True,
                                               lookup_url_kwarg='poll_pk')

    class Meta:
        model = Question
        fields = (
            'id',
            'url',
            'poll',
            'question_text',
            'question_type',
            'published',
            'ago',
            'pub_date',
        )
        read_only_fields = ('pub_date',)

    def get_url(self, obj):
        return str(self.context['request'].build_absolute_uri(obj.id))

    def get_ago(self, obj):
        return naturaltime(obj.pub_date)


class ChoiceListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = (
            'id',
            'url',
            'choice_text',
            'value',
        )
        read_only_fields = ('id',)

    def get_url(self, obj):
        return str(self.context['request'].build_absolute_uri(obj.id) + "/answer/")


class ChoiceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = (
            'id',
            'choice_text',
            'value',
        )
        read_only_fields = ('id',)


class QuestionDetailSerializer(serializers.ModelSerializer):
    ago = serializers.SerializerMethodField()
    answer_numeric_url = serializers.SerializerMethodField()
    answer_date_url = serializers.SerializerMethodField()
    choices = ChoiceListSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'question_text',
            'question_type',
            'choices',
            'answer_numeric_url',
            'answer_date_url',
            'published',
            'ago',
            'pub_date',
        )
        read_only_fields = ('pub_date',)

    def get_ago(self, obj):
        return naturaltime(obj.pub_date)

    def get_answer_numeric_url(self, obj):
        return str(self.context['request'].build_absolute_uri() + "numericanswer/")

    def get_answer_date_url(self, obj):
        return str(self.context['request'].build_absolute_uri() + "dateanswer/")


class AnswerMultipleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = (
            'id',
            'question',
            'poll',
            'choice',
            'numeric_answer',
            'date_answer',
        )

        read_only_fields = ('id', 'question', 'poll',
                            'choice', 'numeric_answer', 'date_answer')

    def create(self, validated_data):
        request = self.context.get('request')
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        poll_pk = self.context.get('view').kwargs.get('poll_pk')
        question_pk = self.context.get(
            'view').kwargs.get('question_pk')
        choice_pk = self.context.get(
            'view').kwargs.get('choice_pk')

        poll = get_object_or_404(Poll, pk=poll_pk)
        question = get_object_or_404(Question, pk=question_pk, poll=poll)
        choice = None
        if question.question_type == 'multiple_choice':
            choice = get_object_or_404(
                Choice, pk=choice_pk, question=question)

            answer = Answer(
                session_id=session_id,
                question=question,
                poll=poll,
                choice=choice,
                numeric_answer=None,
                date_answer=None,
            )
        else:
            raise serializers.ValidationError(
                "This is not a valid type question.")

        try:
            answer.save()
        except:
            answer = get_object_or_404(Answer,
                                       session_id=session_id,
                                       question=question,
                                       poll=poll)
            answer.choice = choice
            answer.save()
        return answer


class AnswerNumericCreateSerializer(serializers.ModelSerializer):
    numeric_answer = serializers.FloatField()

    class Meta:
        model = Answer
        fields = (
            'id',
            'question',
            'poll',
            'choice',
            'numeric_answer',
            'date_answer',
        )

        read_only_fields = ('id', 'question', 'poll', 'choice', 'date_answer')

    def create(self, validated_data):
        request = self.context.get('request')
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        poll_pk = self.context.get('view').kwargs.get('poll_pk')
        question_pk = self.context.get(
            'view').kwargs.get('question_pk')

        poll = get_object_or_404(Poll, pk=poll_pk)
        question = get_object_or_404(Question, pk=question_pk, poll=poll)
        numeric_answer = None
        if question.question_type == 'numeric_input':
            numeric_answer = validated_data['numeric_answer']

            answer = Answer(
                session_id=session_id,
                question=question,
                poll=poll,
                numeric_answer=numeric_answer,
                choice=None,
                date_answer=None,
            )

        try:
            answer.save()
        except:
            answer = get_object_or_404(Answer,
                                       session_id=session_id,
                                       question=question,
                                       poll=poll)
            answer.numeric_answer = numeric_answer
            answer.save()
        return answer


class AnswerDateCreateSerializer(serializers.ModelSerializer):
    date_answer = serializers.DateField()

    class Meta:
        model = Answer
        fields = (
            'id',
            'question',
            'poll',
            'choice',
            'numeric_answer',
            'date_answer',
        )

        read_only_fields = ('id', 'question', 'poll',
                            'choice', 'numeric_answer')

    def create(self, validated_data):
        request = self.context.get('request')
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        poll_pk = self.context.get('view').kwargs.get('poll_pk')
        question_pk = self.context.get(
            'view').kwargs.get('question_pk')

        poll = get_object_or_404(Poll, pk=poll_pk)
        question = get_object_or_404(Question, pk=question_pk, poll=poll)
        date_answer = None
        if question.question_type == 'date_input':
            date_answer = validated_data['date_answer']

            answer = Answer(
                session_id=session_id,
                question=question,
                poll=poll,
                date_answer=date_answer,
                numeric_answer=None,
                choice=None
            )

        try:
            answer.save()
        except:
            answer = get_object_or_404(Answer,
                                       session_id=session_id,
                                       question=question,
                                       poll=poll)
            answer.date_answer = date_answer
            answer.save()
        return answer


class AnswerListSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()
    poll = serializers.StringRelatedField()
    choice = ChoiceDetailSerializer()

    class Meta:
        model = Answer
        fields = (
            'id',
            'session_id',
            'question',
            'poll',
            'choice',
            'numeric_answer',
            'date_answer',
            'score',
        )
        read_only_fields = ('id', 'session_id', 'question', 'poll',
                            'choice', 'numeric_answer', 'date_answer')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'name',
            'short_name',
            'description',
            'aktien',
            'anleihen',
            'investment_horizon',
            'experience',
            'liquidity_needs',
        )

        read_only_fields = (
            'name',
            'short_name',
            'description',
            'aktien',
            'anleihen',
            'investment_horizon',
            'experience',
            'liquidity_needs',
        )


class BitSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Bit
        exclude = ('id', 'published', 'poll')

        read_only_fields = (
            'name',
            'short_name',
            'description',
            'how_invest',
            'motto',
            'behavioral_biases',
            'cognitive_biases',
            'risk_value',
        )


class SessionProfileListSerializer(serializers.ModelSerializer):
    poll = serializers.HyperlinkedRelatedField(view_name='poll-detail',
                                               read_only=True,
                                               lookup_url_kwarg='poll_pk')

    # products = ProductSerializer(many=True, read_only=True)
    bit = BitSerializer(read_only=True)

    class Meta:
        model = SessionProfile
        fields = (
            'id',
            'session_id',
            'poll',
            'bit',
            'profile_calc',
            'potential_investment',
            'horizon',
            'liquidity_needs',
            'investment_experience_years',
            'accepts_profile',
            'creation_date',
        )

        read_only_fields = (
            'id',
            'session_id',
            'poll',
            'bit',
            'products',
            'profile_calc',
            'potential_investment',
            'horizon',
            'liquidity_needs',
            'investment_experience_years',
            'accepts_profile',
            'creation_date',
        )

    def example_calculation(self, other_args):
        pass

    def create(self, validated_data):
        request = self.context.get('request')
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key

        poll_pk = self.context.get('view').kwargs.get('poll_pk')
        poll = get_object_or_404(Poll, pk=poll_pk)

        question = Question.objects.filter(poll=poll)
        total_questions = question.count()

        answers = Answer.objects.filter(session_id=session_id, poll=poll)
        total_answers = answers.count()

        if total_answers < total_questions:
            raise serializers.ValidationError(
                "Please answer all questions for result.")

        total_score = 0
        for answer in answers:
            if answer.score:
                total_score = total_score + answer.score

        # DO CALCULATIONS HERE! DEFINE YOUR FUNCTIONS IN THIS CLASS AND CALL THEM LIKE BELOW

        self.example_calculation(other_args=total_score)

        # get the right product for the user  you can filter them with Product table properties
        try:
            bit = Bit.objects.get(risk_value=total_score,
                                  poll=poll, published=True)
        except Bit.DoesNotExist:
            raise serializers.ValidationError("Bit not found.")

        products = Product.objects.filter(bit=bit)

        if not products:
            raise serializers.ValidationError("Products not found.")

        sessionprofile = SessionProfile(
            session_id=session_id,
            poll=poll,
            bit=bit,
            # user_rating=,
            profile_calc=total_score,  # Add by calculations
            # profile_text=,
            # potential_investment=,
            # horizon=,
            # liquidity_needs=,
            # investment_experience_years=,
            # investment_previous=,
            # accepts_profile=,
            # creation_date=,
        )
        try:
            sessionprofile.save()
            sessionprofile.products.set(products)
            sessionprofile.save()
        except:
            raise serializers.ValidationError("Your result already generated!")
        return sessionprofile
