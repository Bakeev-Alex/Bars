from django.urls import path

from .views import MainViews, QuizViews, EditQuizViews, ResultQuiz

app_name = 'user_tests'

urlpatterns = [
    path('', MainViews.as_view(), name='main'),
    path('quiz/<int:quiz_id>', QuizViews.as_view(), name='quiz'),
    path('processing/', QuizViews.as_view(), name='processing'),

    path('edit_quiz/<int:quiz_id>', EditQuizViews.as_view(), name='edit_quiz'),
    path('create_quiz/', EditQuizViews.as_view(), name='create_quiz'),

    path('result_detail/<str:unique_pk>', ResultQuiz.as_view(), name='result_detail'),
]
