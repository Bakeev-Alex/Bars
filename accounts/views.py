from django.utils.timezone import make_aware

from datetime import datetime
from datetime import date
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import StudentForm, ProfessorForm, AuthenticationUserForm
from user_tests.models import UniqueValue, Quiz


class AuthenticationViews(LoginView):
    form_class = AuthenticationUserForm
    redirect_authenticated_user = True


class ProfessorView(TemplateView):
    template_name = 'accounts/auth_teacher.html'

    def __init__(self):
        super().__init__()
        self.forms = None

    def get(self, request, *args, **kwargs):
        self.forms = ProfessorForm()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.forms = ProfessorForm(request.POST)
        if self.forms.is_valid():
            self.forms.save(commit=False)
            self.forms.save()
            return redirect(reverse('user_tests:main'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = self.forms
        return context


class StudentView(TemplateView):
    template_name = 'accounts/auth_student.html'

    def __init__(self):
        super().__init__()
        self.student_form = None

    def get(self, request, *args, **kwargs):
        self.student_form = StudentForm()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.student_form = StudentForm(request.POST)
        if self.student_form.is_valid():
            self.student_form.save(commit=False)
            self.student_form.save()
            return redirect(reverse('user_tests:main'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['student_form'] = self.student_form
        return context


class StudentAccountViews(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_quiz = UniqueValue.objects.filter(user_id=self.request.user.id)
        paginator = Paginator(user_quiz, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context


class TeacherAccountViews(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/teacher.html'


@login_required
def popular_quiz(request):
    context = {}
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        if date_from:
            date_from = make_aware(datetime.strptime(request.POST.get('date_from'), '%Y-%m-%d'))
        else:
            date_from = date.today()
        if date_to:
            date_to = make_aware(datetime.strptime(request.POST.get('date_to'), '%Y-%m-%d'))
        else:
            date_to = date.today()

        quiz_by_date = UniqueValue.objects.filter(create__gte=date_from, create__lte=date_to).values_list('quiz', flat=True)
        quiz_list = list(set(quiz_by_date))
        quiz_count = {i: list(quiz_by_date).count(i) for i in quiz_list}

        quiz = Quiz.objects.filter(id__in=quiz_list)

        data = []
        for quiz_item in quiz_list:
            obj = quiz.get(id=quiz_item)
            data.append(
                {
                    'quiz': obj,
                    'count_quiz': quiz_count.get(quiz_item)
                }
            )

        context['page_obj'] = data
        context['date_from'] = datetime.strftime(date_from, '%d.%m.%Y')
        context['date_to'] = datetime.strftime(date_to, '%d.%m.%Y')

        return render(request, 'accounts/reports/result_popular.html', context)

    return render(request, 'accounts/reports/popular_quiz.html', context)
