from django.urls import path
from .views import register, login, upload_book, start_quiz, submit_quiz, user_history

urlpatterns = [
    path("auth/register/", register),
    path("auth/login/", login),

    path("books/upload/", upload_book),

    path("quiz/start/", start_quiz),
    path("quiz/submit/", submit_quiz),

    path("quiz/history/<str:user_id>/", user_history),
]