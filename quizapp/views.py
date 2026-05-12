
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from quizapp.serializers import RegisterSerializer
from .models import User, Book
from quizapp.models import  QuizSession
from rest_framework_simplejwt.tokens import RefreshToken
from quizapp.pdf_reader import extract_text_from_pdf
from quizapp.ai_agent import call_ai_generate_questions, call_ai_grade_answers


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = User.objects(email=email).first()
    if not user:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    from django.contrib.auth.hashers import check_password
    if not check_password(password, user.password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "role": user.role,
        "username": user.username,
        "user_id": str(user.id)   # 🔥 أضفنا الـ user_id هون
    })

# Create your views here.
@api_view(["POST"])
def start_quiz(request):
    user_id = request.data["user_id"]
    specialization = request.data["specialization"]
    num_questions = int(request.data.get("num_questions", 10))

    # جلب الكتاب
    book = Book.objects(specialization=specialization).first()

    # استخراج النص
    text = extract_text_from_pdf(book.file_path)

    # توليد الأسئلة عبر Llama3
    ai_questions = call_ai_generate_questions(text, num_questions)

    # إنشاء جلسة
    session = QuizSession(
        user_id=user_id,
        specialization=specialization,
        total_questions=num_questions
    )
    session.save()

    return Response({
        "session_id": str(session.id),
        "questions": ai_questions
    })


@api_view(["POST"])
def submit_quiz(request):
    session_id = request.data["session_id"]
    questions = request.data["questions"]
    answers = request.data["answers"]

    session = QuizSession.objects(id=session_id).first()

    ai_result = call_ai_grade_answers(questions, answers)

    session.score = ai_result["score"]
    session.save()

    return Response({"score": session.score})

@api_view(["POST"])
def upload_book(request):
    title = request.data.get("title")
    specialization = request.data.get("specialization")
    file = request.FILES.get("file")
    user_id = request.data.get("user_id")

    file_path = f"books/{file.name}"
    with open(file_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)

    book = Book(
        title=title,
        specialization=specialization,
        file_path=file_path,
        uploaded_by=user_id
    )
    book.save()

    return Response({"book_id": str(book.id)})
@api_view(["GET"])
def user_history(request, user_id):
    sessions = QuizSession.objects(user_id=user_id).order_by("-created_at")

    return Response([
        {
            "session_id": str(s.id),
            "specialization": s.specialization,
            "score": s.score,
            "total_questions": s.total_questions,
            "created_at": s.created_at
        }
        for s in sessions
    ])