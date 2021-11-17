from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings

from .views import ProfessorView, StudentView, AuthenticationViews, StudentAccountViews, \
    TeacherAccountViews, popular_quiz

app_name = 'accounts'

urlpatterns = [
    path('login/', AuthenticationViews.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('student_auth/', StudentView.as_view(), name='student_auth'),
    path('professor_auth/', ProfessorView.as_view(), name='professor_auth'),

    path('student/<int:student_id>', StudentAccountViews.as_view(), name='student'),
    path('teacher/<int:teacher_id>', TeacherAccountViews.as_view(), name='teacher'),

    path('popular/', popular_quiz, name='popular')
]
