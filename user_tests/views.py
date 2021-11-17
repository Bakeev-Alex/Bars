import secrets
import string

from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Quiz, Question, Variant, UniqueValue, Answer
from .forms import QuizEditForm, QuestionsFormSet, VariantsFormSet


class MainViews(LoginRequiredMixin, TemplateView):
    template_name = 'user_tests/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quizzes = Quiz.objects.filter(is_active=True)
        paginator = Paginator(quizzes, 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class QuizViews(LoginRequiredMixin, TemplateView):
    template_name = 'user_tests/quiz.html'
    queryset_variants = Variant.objects.filter(is_active=True)

    def __init__(self):
        super().__init__()
        self.result_dict = []
        self.unique_pk = ''

    def get(self, request, *args, **kwargs):
        self.unique_pk = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(50))
        request.session['key_test'] = self.unique_pk

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        answer_list = request.POST.getlist('answer')
        quiz = request.POST.get('quiz_id')
        unique_pk = request.session.get('key_test')

        answers = Variant.objects.filter(id__in=answer_list).values('id', 'correct', 'questions')

        unique_value = UniqueValue.objects.get_or_create(
            unique_value=unique_pk,
            defaults={
                'user_id': request.user.id,
                'quiz_id': int(quiz)
            }
        )

        data = []
        for answer_item in answers:
            data.append(Answer(
                unique_id=unique_value[0].id,
                question_id=answer_item.get('questions'),
                variant_id=answer_item.get('id'),
                correct_answer=answer_item.get('correct')
            ))

        Answer.objects.bulk_create(data)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.filter(quiz_id=kwargs.get('quiz_id'))
        context['questions'] = questions
        context['question_item'] = questions.first()
        context['unique_pk'] = self.unique_pk

        return context


class EditQuizViews(LoginRequiredMixin, TemplateView):

    template_name = 'user_tests/edit_quiz.html'

    def __init__(self):
        super().__init__()
        self.form = None
        self.quiz = None

    def get(self, request, *args, **kwargs):
        self.quiz = Quiz.objects.filter(id=kwargs.get('quiz_id')).prefetch_related('questions')

        self.form = QuizEditForm(instance=self.quiz.first())

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        quiz_pk = kwargs.get('quiz_id')
        self.quiz = Quiz.objects.filter(id=quiz_pk).first()
        self.form = QuizEditForm(request.POST, instance=self.quiz)

        if self.form.is_valid():
            self.form = self.form.save(commit=False)

            question_form = QuestionsFormSet(request.POST, instance=self.form)

            if question_form.is_valid():
                question_form.save(commit=False)

                variants = VariantsFormSet(request.POST, instance=question_form)
                if variants.is_valid():
                    variants.save()

                question_form.save()
            self.form.save()
            messages.info(request, 'Success')

            if quiz_pk:
                return redirect(reverse('user_tests:edit_quiz', kwargs={'quiz_id': quiz_pk}))
            else:
                return redirect(reverse('user_tests:create_quiz'))
        else:
            messages.error(request, 'Ошибка в валидации формы')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['variants'] = VariantsFormSet()
        context['question_form'] = QuestionsFormSet()
        context['quiz_pk'] = kwargs.get('quiz_id')

        return context


class ResultQuiz(LoginRequiredMixin, TemplateView):
    template_name = 'user_tests/test_final.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'unique_pk' in kwargs:
            result_unique = UniqueValue.objects.filter(unique_value=kwargs.get('unique_pk')).prefetch_related('result_unique').first()
            context['result_unique'] = result_unique

            context['result_quiz'] = counting_responses(result_unique)

        return context


def counting_responses(results) -> dict:
    user_selection = {}
    for answer in results.result_unique.all():
        question = answer.question_id
        if question not in user_selection:
            user_selection[question] = []
        user_selection[question].append(answer.correct_answer)

    result_answer = {
        'quantity': 0,
        'correct': 0,
        'wrong': 0,
        'percent': 0,
        'assessment': 0
    }
    for question, answer in user_selection.items():
        result_answer['quantity'] += 1
        answer_set = set(answer)
        if len(answer_set) == 1 and True in answer_set:
            result_answer['correct'] += 1
        else:
            result_answer['wrong'] += 1

    try:
        result_answer['percent'] = round((result_answer['correct'] / result_answer['quantity']) * 100, 2)
    except ZeroDivisionError:
        pass

    if result_answer['percent'] <= 50:
        result_answer['assessment'] = 2
    elif 75 >= result_answer['percent'] > 50:
        result_answer['assessment'] = 3
    elif 90 >= result_answer['percent'] > 75:
        result_answer['assessment'] = 4
    else:
        result_answer['assessment'] = 5

    return result_answer
